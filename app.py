import streamlit as st
from PIL import Image
import tensorflow as tf
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
import numpy as np
import cv2
import pickle

# Load pre-trained models and data
@st.cache_resource
def load_assets():
    # preprocess.h5 is a pickled Keras model, not a standard H5 file
    with open("preprocess.h5", "rb") as f:
        preprocess = pickle.load(f)
    
    model = load_model("model_9.h5")
    # Corrected filename from your directory: tokenizer.pkl
    tokenizer = pickle.load(open("tokenizer.pkl", "rb"))
    max_length = pickle.load(open("maxlength.dump", "rb"))
    return preprocess, model, tokenizer, max_length

# Initialize assets
preprocess_model, caption_model, tokenizer, max_length = load_assets()
    

# Function to load an image
def load_image(image_file):
    img = Image.open(image_file)
    return img

# Function to map integer to word using tokenizer
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

# Generate description for an image
def generate_desc(model, tokenizer, photo, max_length):
    in_text = '<start>'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = tf.keras.preprocessing.sequence.pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = word_for_id(yhat, tokenizer)
        if word is None:
            break
        in_text += " " + word
        if word == "end":
            break
    return in_text.replace('<start>', '').replace('end', '').strip()

def main():
    st.title("Welcome to Auto Image Caption Generator")
    menu = ["Image", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Image":
        st.subheader("Upload an image to generate the captions")
        image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
        
        if image_file is not None:
            # Display file info
            file_details = {
                "filename": image_file.name,
                "filetype": image_file.type,
                "filesize": image_file.size
            }
            st.write(file_details)
            
            # 1. Load and Display Image
            img = load_image(image_file)
            st.image(img)

            # 2. Preprocess Image
            img_arr = np.array(img.convert('RGB'))
            new_image = cv2.resize(img_arr, (224, 224))
            image_array = tf.keras.preprocessing.image.img_to_array(new_image)
            image_array = np.expand_dims(image_array, axis=0)
            image_array = preprocess_input(image_array)
            
            # 3. Extract Features and Generate Caption
            with st.spinner("Analyzing image..."):
                features = preprocess_model.predict(image_array, verbose=0)
                yhat = generate_desc(caption_model, tokenizer, features, max_length)
                st.markdown(f"### Result: \n {yhat.capitalize()}")

    elif choice == "About":
        st.subheader("About Project")

if __name__ == "__main__":
    main()