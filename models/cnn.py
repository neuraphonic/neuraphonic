from torchvision.models import vit_b_16, ViT_B_16_Weights
import torch
from torch import nn

model = vit_b_16(weights=ViT_B_16_Weights.IMAGENET1K_V1)

parameters = model.parameters()

for p in parameters:
    p.requires_grad = False

num_classes = 2

model.heads = nn.Sequential(nn.Linear(in_features=768, out_features=num_classes), nn.Softmax(dim=1))

def step(model, train, optimizer, loss_fn):
    model.train()
    total_loss = 0
    total_acc = 0
    for x, y in train:
        y_pred = model(x)
        loss = loss_fn(y_pred, y)
        total_loss += loss.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_acc += (y_pred == y).sum().item()/len(y_pred)

    train_loss = total_loss / len(train)
    train_acc = total_acc / len(train)

    return train_loss, train_acc

def test(model, test, loss_fn):
    model.eval()
    total_loss = 0
    total_acc = 0

    with torch.inference_mode():
        for x, y in test:
            y_pred = model(x)
            loss = loss_fn(y_pred, y)
            total_loss += loss.item() 
            total_acc += (y_pred == y).sum().item()/len(y_pred)
    
    test_loss = total_loss / len(train)
    test_acc = total_acc / len(train)

    return test_loss, test_acc

def train(model, train, test, optimizer, loss_fn, epochs):
    for epoch in range(epochs):
        _, train_acc = step(model, train, optimizer, loss_fn)
        _, test_acc = test(model, test, loss_fn)

        print("Epoch " + str(epoch) + ", Accuracies: " + str(train_acc) + ", " + str(test_acc))

