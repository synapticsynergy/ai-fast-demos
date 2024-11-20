import streamlit as st
import requests
from PIL import Image
import os
from pathlib import Path
import numpy as np
from streamlit_image_select import image_select

# Hide deploy button
st.markdown(
    r"""
    <style>
    .stAppDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)


def load_images_from_folder(folder_path):
    """Load all images from a folder"""
    images = {}
    valid_extensions = {'.jpg', '.jpeg', '.png'}

    for file in Path(folder_path).glob('*'):
        if file.suffix.lower() in valid_extensions:
            images[file.name] = str(file)
    return images


def create_image_grid(images_dict):
    if "uploaded_file" in st.session_state and not st.session_state["uploaded_file"]:
        images_list = list(images_dict.items())
        img = image_select(
            label="",
            # Not including the last image to make the grid look cleaner
            images=list(map(lambda x: x[1], images_list))[0:len(images_list)-1],
            # captions=["", "", "", "", ""],
        )
        return img
    return None


def get_prediction(image_path, api_url):
    """Get prediction from FastAPI server"""
    files = {'file': open(image_path, 'rb')}
    try:
        response = requests.post(api_url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to server: {str(e)}")
        return None


def get_uploaded_file_prediction(file, api_url):
    """Get prediction from FastAPI server"""
    files = {'file': file}  # Send the file object directly
    try:
        response = requests.post(api_url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to server: {str(e)}")
        return None


def main():
    st.title("Image Classification UI")

    # Configuration
    IMAGES_FOLDER = "assets/image_class_options"
    API_URL = "http://localhost:8000/classify_image"  # Update if your API is hosted elsewhere

    # Initialize session state
    if 'selected_image' not in st.session_state:
        st.session_state.selected_image = None
    if 'prediction_result' not in st.session_state:
        st.session_state.prediction_result = None

    # Load images
    images = load_images_from_folder(IMAGES_FOLDER)

    uploaded_file = st.file_uploader("Or upload a picture of a flower", type=["jpg", "jpeg", "png"], key="uploaded_file")

    if "uploaded_file" in st.session_state and not st.session_state["uploaded_file"]:
        st.subheader("Select an Image")
    selected = create_image_grid(images)

    if selected:
        st.session_state.selected_image = selected
        st.session_state.prediction_result = None


    if "uploaded_file" in st.session_state and st.session_state["uploaded_file"]:
        st.subheader("Selected Image")
        st.image(uploaded_file, caption="Uploaded Image")

        # Add some spacing
        st.write("")

        # Prediction button
        if st.button("Get Prediction", type="primary", use_container_width=True):
            with st.spinner("Getting prediction..."):
                print(f"Getting prediction for {uploaded_file}")
                result = get_uploaded_file_prediction(uploaded_file, API_URL)
                st.session_state.prediction_result = result

        # Display prediction result
        if st.session_state.prediction_result:
            st.markdown("---")
            result = st.session_state.prediction_result
            st.success(f"Predicted Class: {result['predicted_class']}")
            score = float(max(result['confidence_scores']))
            st.write(f"Confidence Score:  {score:.1%}")

    elif st.session_state.selected_image:
        path = st.session_state.selected_image

        st.subheader("Selected Image")
        img = Image.open(path)
        st.image(img, caption="", use_container_width=True)

        # Check if this image is selected
        is_selected = st.session_state.get('selected_image') == path

        # Add some spacing
        st.write("")

        # Prediction button
        if st.button("Get Prediction", type="primary", use_container_width=True):
            with st.spinner("Getting prediction..."):
                print(f"Getting prediction for {uploaded_file}")
                result = get_prediction(path, API_URL)
                st.session_state.prediction_result = result

        # Display prediction result
        if st.session_state.prediction_result:
            st.markdown("---")
            result = st.session_state.prediction_result
            st.success(f"Predicted Class: {result['predicted_class']}")
            score = float(max(result['confidence_scores']))
            st.write(f"Confidence Score:  {score:.1%}")


main()