import torch
import copy
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import torchvision
import torchvision.models.quantization as models
from torchvision import transforms, datasets
from torch import nn
from torch.quantization import convert


# Followed a tutorial on quantization on pytorch's home page.
# https://pytorch.org/tutorials/intermediate/quantized_transfer_learning_tutorial.html
# Made a few modifications by adding a few functions for example the,
# load_data function. The original tutorial had all of the variables,
# that's inside that function as global variables,
# same goes for the setup_model function i also added a main function.

# For some reason my training of the model is faster then the tutorial,
# says it should be. They say it should take between 15-25 min to train it,
# mine only takes around 8 mins. The original train function even uses,
# more threads/num_workers then mine does and mine is still faster


# Create a function that loads data transforms using dataloaders and
# the built in datasets and also adds some classes so you can classify the data
def load_data(data_dir):
    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize(256),
            transforms.RandomCrop(256),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.225, 0.224])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.RandomCrop(256),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.225, 0.224])
        ]),
    }

    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                              data_transforms[x])
                      for x in ['train', 'val']}
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x],                                                              batch_size=16,
                                                  shuffle=True, num_workers=4)

                   for x in ['train', 'val']}
    dataset_sizes = {x: len(image_datasets[x])

                     for x in ['train', 'val']}
    class_names = image_datasets['train'].classes

    return dataloaders, dataset_sizes, class_names


# Create a helper function for the subplot,
# which uses numpy to set the input for the making of a grid that,
# the subplot will use to display the predictions made by the AI model
def imshow(inp, title=None, ax=None, figsize=(5, 5)):

    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.225, 0.224])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)

    if ax is None:
        fig, ax = plt.subplots(1, figsize=figsize)

    ax.imshow(inp)
    ax.set_xticks([])
    ax.set_yticks([])

    if title is not None:
        ax.set_title(title)


# This is the function that actually trains the AI model
def train_model(model, criterion, optimizer, scheduler, num_epochs=25,
                device='cpu'):

    data_dir = 'data/hymenoptera_data'
    dataloaders, dataset_sizes, class_names = load_data(data_dir)
    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print('Epoch {}|{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:

                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)
                    if phase == 'train':
                        scheduler.step()

                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects.double() / dataset_sizes[phase]

                print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                    phase, epoch_loss, epoch_acc))

                if phase == 'val' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())

                print()

                time_elapsed = time.time() - since
                print('Training complete in {:.0f}m {:.0f}s'.format(
                    time_elapsed // 60, time_elapsed % 60))
                print('Best val Acc: {:4f}'.format(best_acc))

    model.load_state_dict(best_model_wts)

    return model


# This is the function that will load the images and creation of the,
# subplot so you can actually see the result and how accurate the predictions,
# that the AI model made is.
def visualize_model(model, dataloaders, class_names, rows=3, cols=3):

    was_training = model.training
    model.eval()
    current_row = current_col = 0
    fig, ax = plt.subplots(rows, cols, figsize=(cols*2, rows*2))

    with torch.no_grad():

        for imgs, lbls in dataloaders['val']:

            imgs = imgs.cpu()
            lbls = lbls.cpu()

            outputs = model(imgs)
            _, preds = torch.max(outputs, 1)

            for jdx in range(imgs.size(0)):
                imshow(imgs.data[jdx], title='predicted: {}'.format(
                    class_names[preds[jdx]]), ax=ax[current_row, current_col])
                ax[current_row, current_col].axis('off')

                current_col += 1
                if current_col >= cols:
                    current_row += 1
                    current_col = 0
                if current_row >= rows:
                    model.train(mode=was_training)
                    return
    model.train(mode=was_training)


# Setup the pretrained model resnet18 that we will use to further train our
# model and not just the custom head
def setup_model():

    # Use the pretrained resnet18 as the neural network,
    model_fe = models.resnet18(pretrained=True, progress=True, quantize=False)

    # Numbers of features to use from the neural network
    num_ftrs = model_fe.fc.in_features

    # Train the model
    model_fe.train()

    # Fuse the model with a custom head
    model_fe.fuse_model()

    return model_fe, num_ftrs


MODEL_FE, NUM_FTRS = setup_model()


# Create a model with a custom head
def create_combined_model(MODEL_FE):
    model_fe = MODEL_FE
    num_ftrs = NUM_FTRS

    model_fe_features = nn.Sequential(
        model_fe.quant,
        model_fe.conv1,
        model_fe.bn1,
        model_fe.relu,
        model_fe.maxpool,
        model_fe.layer1,
        model_fe.layer2,
        model_fe.layer3,
        model_fe.layer4,
        model_fe.avgpool,
        model_fe.dequant,
    )

    head = nn.Sequential(
        nn.Dropout(p=0.5),
        nn.Linear(num_ftrs, 2),
    )

    model = nn.Sequential(
        model_fe_features,
        nn.Flatten(1),
        head,
    )

    return model


# Just a main function that calls all the functions above it
def main():

    data_dir = 'data/hymenoptera_data'

    dataloaders, dataset_sizes, class_names = load_data(data_dir)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    inputs, classes = next(iter(dataloaders['train']))

    out = torchvision.utils.make_grid(inputs, nrow=4)

    fig, ax = plt.subplots(1, figsize=(10, 10))

    imshow(out, title=[class_names[x] for x in classes], ax=ax)

    model = create_combined_model(MODEL_FE)

    model = model.to(device)

    criterion = torch.nn.CrossEntropyLoss()

    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer, step_size=7,                                                         gamma=0.1)

    trained_model = train_model(model, criterion, optimizer, scheduler,
                                num_epochs=25, device=device)
    trained_model.cpu()

    model_quantized_and_trained = convert(trained_model, inplace=False)

    visualize_model(model_quantized_and_trained, dataloaders, class_names)

    plt.ioff()

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
