# Description: This script loads a pre-trained TensorFlow model and uses it to make predictions on images.

import tensorflow as tf
import json

# Load model
loaded_model = tf.keras.models.load_model("./resources/model.h5")

# Check if the model is loaded correctly
# loaded_model.summary()

# Check class names
with open("./resources/labels.json", "r") as f:
    labels = json.load(f)

# Function to load an image and resize it for model input
def load_and_prep_image(filename, img_shape=224):
    """
    Loads an image from a file, converts it to a tensor, centrally crops it,
    resizes it to (img_shape, img_shape), and normalizes pixel values.

    Parameters:
    filename (str): Path to the image file.
    img_shape (int): Desired width and height after resizing. Default is 224.

    Returns:
    tf.Tensor: Preprocessed image tensor.
    """

    # Read the image
    img = tf.io.read_file(filename)

    # Decode the image file into a tensor
    img = tf.image.decode_image(img)

    # Centrally crop the image to a square
    shape = tf.shape(img)
    height, width = shape[0], shape[1]
    crop_size = tf.minimum(height, width)

    offset_height = (height - crop_size) // 2
    offset_width = (width - crop_size) // 2
    img = tf.image.crop_to_bounding_box(img, offset_height, offset_width, crop_size, crop_size)

    # Resize the image to the desired shape
    img = tf.image.resize(img, size=[img_shape, img_shape])

    # Normalize the pixel values to the range [0, 1]
    img = img / 255.
    return img

# Define a function to make predictions
def predict(image_path):
    """
    Predicts the class of an image using a pre-trained model.
    Parameters:
    image_path (str): Path to the image file.
    Returns:
    int: Predicted class index.
    """

    # Load and preprocess the image
    img = load_and_prep_image(image_path)

    pred = loaded_model.predict(tf.expand_dims(img, axis=0))

    # Get the predicted class
    predicted_class = tf.argmax(pred, axis=1).numpy()[0]
    
    # Get the predicted label
    predicted_class_name = labels[predicted_class]

    return predicted_class_name

