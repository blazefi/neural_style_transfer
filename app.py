import streamlit as st
import streamlit.components.v1 as stc
from os import walk, path
import os
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image


def load_image(image_file):
    img = Image.open(image_file).convert("RGB")
    
    im1 = img.save("temp.jpg")
    img = tf.io.read_file("./temp.jpg")
    os.remove("./temp.jpg") 
    return img

def preprocess_image(img):
    img = tf.image.decode_image(img, channels=3)        # making sure image has 3 channels
    img = tf.image.convert_image_dtype(img, tf.float32) # making sure image has dtype float 32
    img = img[tf.newaxis, :]
    return img




def main():
    st.title("Neural Style Transfer")
    model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

     

    st.subheader("Upload Images")
    st.write("** Note : Select only two images **")
    st.write("*** First select the source image and then select the style image. ***")

    images = st.file_uploader("Upload Image", type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)
    
    if st.button("Process"):
        if images is not None:
            
            content_image = load_image(images[0])
            style_image = load_image(images[1])
            content_image = preprocess_image(content_image)
            style_image = preprocess_image(style_image)
            
            stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]
            st.image((np.squeeze(stylized_image)))
            
            

if __name__ == '__main__':
    main()
