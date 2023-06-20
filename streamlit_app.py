import streamlit as st
from rembg import remove
from PIL import Image
import io
import tempfile
import os

def remove_background(image_path):
    with open(image_path, "rb") as f:
        img = f.read()
        output = remove(img)

    processed_image = Image.open(io.BytesIO(output)).convert("RGBA")
    return processed_image

def main():
    st.title("Background Removal App")
    st.write("Upload an image and remove the background")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Save uploaded file to temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        temp_file.close()  # Close the file before removing it

        # Display original image
        original_image = Image.open(uploaded_file)
        st.image(original_image, caption="Original Image", use_column_width=True)

        # Remove background and display processed image
        with st.spinner('Processing...'):
            processed_image = remove_background(temp_file.name)

        # Display processed image
        st.image(processed_image, caption="Processed Image", use_column_width=True)

        # Download button
        buffered = io.BytesIO()
        processed_image.save(buffered, format="PNG")
        b64_image = buffered.getvalue()
        st.download_button("Download Processed Image", data=b64_image, file_name="processed_image.png")

        # Remove temporary file
        os.remove(temp_file.name)

if __name__ == "__main__":
    main()
