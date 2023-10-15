from torchvision.models import vit_b_16, ViT_B_16_Weights
import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchvision import transforms, datasets


# transform = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor()])

# dataset = datasets.ImageFolder('data/spectrograms', transform=transform)

# data_len = len(dataset)
# train_len = int(data_len*0.8)
# test_len = data_len - train_len

# train_set, test_set = random_split(dataset, [train_len, test_len])

# train_set = DataLoader(train_set, batch_size=32, shuffle=True)
# test_set = DataLoader(test_set, batch_size=32, shuffle=True)

# model = vit_b_16(weights=ViT_B_16_Weights.IMAGENET1K_V1)

# parameters = model.parameters()

# for p in parameters:
#     p.requires_grad = False

# num_classes = 2

# model.heads = nn.Sequential(nn.Linear(in_features=768, out_features=num_classes), nn.Softmax(dim=1))

# parameters = model.parameters()

def step(model, train_set, optimizer, loss_fn):
    model.train()
    total_loss = 0
    total_acc = 0
    for _, (x, y) in enumerate(train_set):
        y_pred = model(x)
        loss = loss_fn(y_pred, y)
        total_loss += loss.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        y_class = torch.argmax(y_pred, dim=1)
        total_acc += (y_class == y).sum().item()/len(y_pred)

    train_loss = total_loss / len(train_set)
    train_acc = total_acc / len(train_set)

    return train_loss, train_acc

def test(model, test_set, loss_fn):
    model.eval()
    total_loss = 0
    total_acc = 0

    with torch.inference_mode():
        for _, (x, y) in enumerate(test_set):
            y_pred = model(x)
            loss = loss_fn(y_pred, y)
            total_loss += loss.item() 
            y_class = torch.argmax(y_pred, dim=1)
            total_acc += (y_class == y).sum().item()/len(y_pred)
    
    test_loss = total_loss / len(test_set)
    test_acc = total_acc / len(test_set)

    return test_loss, test_acc

def train_loop(model, train_set, test_set, optimizer, loss_fn, epochs):
    for epoch in range(epochs):
        train_loss, _ = step(model, train_set, optimizer, loss_fn)
        _, test_acc = test(model, test_set, loss_fn)

        print("Epoch " + str(epoch + 1) + ", Loss: " + str(train_loss) + ", Accuracy: " + str(test_acc))

# train_loop(model, train_set, test_set, torch.optim.SGD(parameters, lr=0.003, momentum=0.9), nn.CrossEntropyLoss(), 10)

# model = vit_b_16(weights=ViT_B_16_Weights.IMAGENET1K_V1)
# model.heads = nn.Sequential(nn.Linear(in_features=768, out_features=2), nn.Softmax(dim=1))

# model.load_state_dict(torch.load("models/vit.pth"))

# torch.save(model, 'models/vit.pth')