import pandas as pd
from joblib import load
from filters.praat import Praat
import torch
import torch.nn as nn
from torchvision.models import vit_b_16, ViT_B_16_Weights
from torchvision import transforms, datasets
import numpy as np

import os

def classify_using_pytorch(audio_sample, is_cloud=True):

    prefix = "/tmp/" if is_cloud else "/data/"
    filepath = os.path.join(prefix, "spectrograms/0")
    os.makedirs(filepath, exist_ok=True)

    # model = vit_b_16(weights=ViT_B_16_Weights.IMAGENET1K_V1)
    # model.heads = nn.Sequential(nn.Linear(in_features=768, out_features=2), nn.Softmax(dim=1))
    model = torch.load("models/vit.pth")
    print("loaded model")

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
    model = load("models/randomforest.joblib")
    praat = Praat()
    features = praat.getFeatures(audio_sample, 75, 200)
    df = pd.DataFrame([features])
    label = model.predict(df)[0]
    print(label)
    return label

def classify(audio_sample, is_cloud=True):
    output1, label1 = classify_using_pytorch(audio_sample, is_cloud)
    label2 = classify_using_saved_model(audio_sample)

    probability = output1

    if (label2 == 1):
        probability = (1 + probability) / 2

    if (label1 == label2 and probability > 0.9):
        return label1, probability
    else:
        return 0, probability
