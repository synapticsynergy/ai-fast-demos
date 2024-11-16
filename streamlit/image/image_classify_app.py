import streamlit as st
import requests
from PIL import Image
import os
from pathlib import Path
import numpy as np

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

def create_image_grid(images_dict, cols=4):
    """Create a grid of clickable images"""
    images_list = list(images_dict.items())
    n_images = len(images_list)
    rows = (n_images + cols - 1) // cols

    # Add CSS for hover effect and selection highlight
    st.markdown("""
        <style>
        .image-container {
            cursor: pointer;
            position: relative;
            padding: 5px;
            border: 2px solid transparent;
            border-radius: 5px;
            transition: transform 0.2s;
        }
        .image-container:hover {
            transform: scale(1.02);
        }
        .selected {
            border-color: #FF4B4B;
        }
        </style>
    """, unsafe_allow_html=True)

    for row in range(rows):
        row_cols = st.columns(cols)
        for col in range(cols):
            idx = row * cols + col
            if idx < n_images:
                name, path = images_list[idx]
                with row_cols[col]:
                    img = Image.open(path)
                    img.thumbnail((200, 200))

                    # Create a unique key for this image
                    key = f"img_{idx}"

                    # Check if this image is selected
                    is_selected = st.session_state.get('selected_image') == (path, name)

                    # Create a clickable container
                    if st.button(
                        "Select",
                        key=key,
                        help=f"Click to select {name}",
                        use_container_width=True
                    ):
                        return path, name

                    # Display the image (non-clickable, but part of the same container)
                    st.image(img, caption=name, use_container_width=True)

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

def main():
    st.title("Image Classification UI")

    # Configuration
    IMAGES_FOLDER = "assets/image_class_options" # Update this
    API_URL = "http://localhost:8000/classify_image"  # Update if your API is hosted elsewhere

    # Initialize session state
    if 'selected_image' not in st.session_state:
        st.session_state.selected_image = None
    if 'prediction_result' not in st.session_state:
        st.session_state.prediction_result = None

    # Load images
    images = load_images_from_folder(IMAGES_FOLDER)

    # Create two columns for layout
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("Select an Image")
        selected = create_image_grid(images)

        if selected:
            st.session_state.selected_image = selected
            st.session_state.prediction_result = None

    with right_col:
        if st.session_state.selected_image:
            path, name = st.session_state.selected_image

            st.subheader("Selected Image")
            st.image(Image.open(path), caption=name)

            # Add some spacing
            st.write("")

            # Prediction button
            if st.button("Get Prediction", type="primary", use_container_width=True):
                with st.spinner("Getting prediction..."):
                    result = get_prediction(path, API_URL)
                    st.session_state.prediction_result = result

            # Display prediction result
            if st.session_state.prediction_result:
                st.markdown("---")
                result = st.session_state.prediction_result
                st.success(f"Predicted Class: {result['predicted_class']}")

                st.write("Confidence Scores:")
                scores = result['confidence_scores']
                for idx, score in enumerate(scores):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.progress(score)
                    with col2:
                        st.write(f"{score:.1%}")


main()