import pandas as pd
from filters.praat import Praat
import torch
from torchvision import transforms, datasets
from joblib import load

import os

def classify_using_pytorch(audio_sample, is_cloud=True):

    prefix = "/tmp/" if is_cloud else "/data/"
    filepath = os.path.join(prefix, "spectrograms/0")
    os.makedirs(filepath, exist_ok=True)

    if not is_cloud:
        model = torch.load("models/vit.pth")
        print("loaded model")
    else:
        model = None
        print("did not load model because this is cloud")

    model.eval()
    praat = Praat()
    praat.generateSpectrogram(audio_sample, filepath)

    transform = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor()])

    image = datasets.ImageFolder(os.path.join(prefix, "spectrograms"), transform=transform)

    image = image[0][0].unsqueeze(0)

    output = model.forward(image)

    label = torch.argmax(output).item()

    return output.detach().numpy()[0][1], label


def classify_using_saved_model(audio_sample):
    praat = Praat()
    features = praat.getFeatures(audio_sample, 75, 200)
    df = pd.DataFrame([features])
    model = load("models/randomforest.joblib")
    label = model.predict(df)[0]
    score = model.predict_proba(df)[0][label]
    print(label, score)
    return label, score

def classify(audio_sample, is_cloud=True):
    if is_cloud:
        print("only using randomforest model")
        return classify_using_saved_model(audio_sample)

    else:
        output2, label2 = classify_using_saved_model(audio_sample)
        output1, label1 = classify_using_pytorch(audio_sample, is_cloud)

        probability = (output2 + output1) / 2
            
        if (label1 == label2):
            return label1, probability
        else:
            return 0, probability
