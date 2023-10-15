import pandas as pd
from joblib import load
from filters.praat import Praat
import torch
import torch.nn as nn
from torchvision.models import vit_b_16, ViT_B_16_Weights
from torchvision import transforms, datasets

import os

def classify_using_pytorch(audio_sample):

    try:
        os.mkdir('data/spectrograms/0')
    except:
        pass

    model = vit_b_16(weights=ViT_B_16_Weights.IMAGENET1K_V1)
    model.heads = nn.Sequential(nn.Linear(in_features=768, out_features=2), nn.Softmax(dim=1))

    model.eval()
    praat = Praat()
    praat.generateSpectrogram(audio_sample, "data/spectrograms/0")

    transform = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor()])

    image = datasets.ImageFolder('data/spectrograms', transform=transform)

    image = image[0][0].unsqueeze(0)

    output = model.forward(image)

    print(output)

    label = torch.argmax(output).item()

    print(label)

    return label


def classify_using_saved_model(audio_sample):
    model = load("models/randomforest.joblib")
    praat = Praat()
    features = praat.getFeatures(audio_sample, 75, 200)
    df = pd.DataFrame([features])
    label = model.predict(df)[0]
    print(label)
    return label

def classify(audio_sample):
    label1 = classify_using_pytorch(audio_sample)
    label2 = classify_using_saved_model(audio_sample)

    if (label1 == label2):
        return label1
    else:
        return 0
