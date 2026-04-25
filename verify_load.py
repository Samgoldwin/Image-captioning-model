import sys
sys.path.insert(0, r'C:\temp_lib')
import os
import pickle
import numpy as np
try:
    import keras
    from keras.models import load_model, Model
    from keras.applications.vgg16 import VGG16, preprocess_input
    from keras.preprocessing.image import load_img, img_to_array
    from keras.preprocessing.sequence import pad_sequences
    print("Keras imported successfully")
except ImportError:
    print("Keras/TensorFlow not found")

try:
    with open('maxlength.dump', 'rb') as f:
        max_length = pickle.load(f)
    print(f"Max length: {max_length}")
except Exception as e:
    print(f"Error loading maxlength: {e}")

try:
    with open('tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    print("Tokenizer loaded successfully")
except Exception as e:
    print(f"Error loading tokenizer: {e}")

try:
    model = load_model('model_9.h5')
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
