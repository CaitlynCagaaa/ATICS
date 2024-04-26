import torch
import torchvision
import torch.nn as nn
import torchvision.models as models
import torch.optim as optim
from torchvision import datasets
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.model_selection import train_test_split
import torch.onnx
import multiprocessing

# Define the root directory where your data is stored.
data_root = r"C:\Users\Steven\Desktop\HiLineTrainingData"

# Create a list of classes (subdirectories) in your data directory.
classes = os.listdir(data_root)

# Initialize empty lists to store training and testing datasets.
train_data = []  # List to store training data file paths.
test_data = []   # List to store testing data file paths.

# Define the ratio for splitting the data (e.g., 75% training, 25% testing).
train_ratio = 0.75

# Iterate through each class (subdirectory) in the data directory.
for class_name in classes:
    class_dir = os.path.join(data_root, class_name)  # Full path to the class directory.
    class_images = os.listdir(class_dir)  # List of image file names in the class directory.

    # Split the class images into training and testing sets using train_test_split.
    train_images, test_images = train_test_split(class_images, train_size=train_ratio, random_state=42)

    # Add the full path to each image in the class directory to the corresponding lists.
    train_data.extend([os.path.join(class_dir, image) for image in train_images])  # Training data file paths.
    test_data.extend([os.path.join(class_dir, image) for image in test_images])     # Testing data file paths.

# Define the data transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize images to 224x224 pixels.
    transforms.ToTensor(),          # Convert images to PyTorch tensors.
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalize pixel values.
])

# Create datasets and data loaders for training and testing.
batch_size = 4

# Create a training dataset and data loader.
trainset = datasets.ImageFolder(data_root, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=2)

# Create a testing dataset and data loader.
testset = datasets.ImageFolder(data_root, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=True, num_workers=2)

# Define class labels
labels = classes

# Load a pre-trained ResNet model
resnet = models.resnet18()

# Get the number of features in the last layer of the ResNet model
num_ftrs = resnet.fc.in_features

# Modify the final fully connected layer to match the number of classes in your dataset
resnet.fc = nn.Linear(num_ftrs, len(classes))

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(resnet.parameters(), lr=0.001, momentum=0.9)

# Training loop
def train(net, trainloader, criterion, optimizer, num_epochs):
    for epoch in range(num_epochs):
        running_loss = 0.0  # Initialize the running loss
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data  # Get the inputs and labels from the data loader

            optimizer.zero_grad()  # Zero the gradients

            # Forward pass
            outputs = net(inputs)  # Pass the inputs through the neural network
            loss = criterion(outputs, labels)  # Calculate the loss
            loss.backward()  # Backpropagate the gradients
            optimizer.step()  # Update the model's parameters

            running_loss += loss.item()  # Add the loss to the running total
            if i % 100 == 99:  # Print every 100 batches
                print(f"[{epoch + 1}, {i + 1}] loss: {running_loss / 100:.3f}")  # Print the average loss
                running_loss = 0.0  # Reset the running loss

# Number of training epochs
num_epochs = 20

if __name__ == '__main__':
    multiprocessing.freeze_support()  # Ensure multiprocessing is properly initialized on Windows
    train(resnet, trainloader, criterion, optimizer, num_epochs)

def evaluate(net, testloader, num_correct_examples=5):
    correct = 0
    total = 0
    correct_examples = []

    # Start of the evaluation function. It takes a neural network (net),
    # a data loader for the test set (testloader), and an optional argument
    # for the number of correctly classified examples to display.

    with torch.no_grad():
        # Use "torch.no_grad()" to disable gradient tracking, as we are not
        # interested in computing gradients during evaluation.

        for data in testloader:
            # Iterate through the test data loader, which provides batches
            # of test images and their corresponding labels.

            inputs, labels = data
            # Get the inputs (images) and their true labels from the current batch.

            outputs = net(inputs)
            # Pass the inputs through the neural network to get predicted outputs.

            _, predicted = torch.max(outputs.data, 1)
            # Determine the predicted labels by selecting the class with
            # the highest probability for each input image.

            total += labels.size(0)
            # Increment the 'total' count by the number of labels in the batch.
            correct += (predicted == labels).sum().item()
            # Increment the 'correct' count by the number of correctly predicted
            # labels in the batch.

            if len(correct_examples) < num_correct_examples:
                # If we haven't collected enough examples yet,
                correct_mask = predicted == labels
                # Create a mask to identify correct predictions in the batch.
                for i in range(len(correct_mask)):
                    if correct_mask[i]:
                        # Iterate through the mask and add correctly classified
                        # examples to the 'correct_examples' list.
                        image = inputs[i].permute(1, 2, 0)
                        # Extract the image and permute the dimensions to be suitable
                        # for displaying with Matplotlib.
                        true_label = labels[i].item()
                        # Get the true label for the image.
                        predicted_label = predicted[i].item()
                        # Get the predicted label for the image.
                        correct_examples.append((image, true_label, predicted_label))
                        # Append the correctly classified example as a tuple.

    accuracy = 100 * correct / total
    # Calculate the accuracy as the percentage of correctly classified examples.
    print(f"Accuracy on the test set: {accuracy:.2f}%")
    # Print the accuracy on the test set.

    print("Correctly classified examples:")
    # Print a message to indicate that the following lines will display
    # correctly classified examples.

    for i, (image, true_label, predicted_label) in enumerate(correct_examples):
        if i >= num_correct_examples:
            break
        # Iterate through the collected correct examples and display them.

        plt.imshow(image)
        # Display the image using Matplotlib.
        plt.title(f"True Label: {true_label}, Predicted Label: {predicted_label}")
        # Set the title of the displayed image to show the true and predicted labels.
        plt.show()
        # Show the image with the title.

# ONNX export code
if __name__ == '__main__':
    evaluate(resnet, testloader)
    # Ensure the model is in evaluation mode before exporting to ONNX
    resnet.eval()

    # Define the path for saving the ONNX file
    ONNX_PATH = r"C:\Users\Steven\Desktop\onnxfile\hiline_class.onnx"

    # Export the model to ONNX format
    torch.onnx.export(resnet, torch.randn(1, 3, 224, 224), ONNX_PATH, verbose=True)