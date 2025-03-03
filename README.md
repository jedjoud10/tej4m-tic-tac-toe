# Task
Simple Tic Tac Toe AI with some machine learning vision / pattern recognition. Allows you to play against it by playing on a white board with LEDs under it

Original source code used was from [here](https://github.com/samyakmohelay/Dog-Breed-Image-Prediction), but instead modified to work with our images and required parameters. Built a custom Keras model for it to work accurately. 

# Installation
Tested only on Windows 11 (with CPU side inference used for TensorFlow)
Used pip to download required packages automatically, did no manual versioning stuff

Python version: 3.12.4
Pip version: 24.0
TF Version: 2.18.0
TF hub Version: 0.16.1

Download ``tic-tac-toe-images.zip`` from [here](https://drive.google.com/file/d/1zOzkzrH54HQYHtl2KO6aTReyYVQoxOM8/view?usp=drive_link) and unzip it inside the project folder. It should unzip to a single ``images`` folder where all images are contained within it. All the images contain a full board of either ``x``s or ``empty`` cells. We then split these into 3x3 cells automatically right before we train the model on it.

## Missing
* Retrieve dedicated server code and upload it
* Retrieve Raspberry Pi LED code