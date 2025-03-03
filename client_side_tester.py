from time import sleep
import pandas as pd
import numpy as np
import os
import tensorflow as tf
import tf_keras as keras
import tensorflow_hub as hub

def load_model(path):
  print(f"Loading saved model from: {path} ...")
  model_path = os.getcwd() + "/" + path
  model = tf.keras.models.load_model(model_path, custom_objects={"KerasLayer":hub.KerasLayer})
  return model

new_model = load_model("models-ttt.h5")

IMG_SIZE = 64

image = tf.io.read_file("image2.jpg")
image = tf.image.decode_jpeg(image,channels=3)
print("Decoded image!")
image = tf.image.convert_image_dtype(image,dtype=tf.float32)
image = tf.image.resize(image, (IMG_SIZE*3, IMG_SIZE*3))
image = tf.constant(tf.expand_dims(image, axis=0))

left = 0.05
right = 0.85
crop_boxes = [[0, left, 1.0, right]]
image = tf.image.crop_and_resize(image, crop_boxes, [0], [IMG_SIZE*3, IMG_SIZE*3])

image = tf.image.extract_patches(
        image,
        sizes=(1, IMG_SIZE, IMG_SIZE, 1),
        strides=[1, IMG_SIZE, IMG_SIZE, 1],
        rates=[1, 1, 1, 1],
        padding='VALID')
image = tf.reshape(image, [1, 9, IMG_SIZE, IMG_SIZE, 3])
image = tf.image.adjust_contrast(image, 2.0)
image = tf.image.adjust_saturation(image, 0.0)
batches = image[0]
predictions = new_model.predict(batches,verbose = 1)
outputs = [0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in range(9):
  outputs[i] = ["bg", "x"][np.argmax(predictions[i])]
print(predictions)
print(outputs)
        

