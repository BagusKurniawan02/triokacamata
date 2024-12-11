import streamlit as st
from PIL import Image
import io

# Fungsi untuk memuat gambar
def load_image(image_file):
    img = Image.open(image_file)
    return img

# Fungsi untuk merotasi gambar
def rotate_image(img, angle):
    return img.rotate(angle, expand=True)

# Fungsi untuk mengonversi gambar ke format byte agar bisa di-download
def convert_image_to_bytes(img, format_type):
    img_byte_arr = io.BytesIO()
    if format_type == "PNG":
        img.save(img_byte_arr, format='PNG')
    elif format_type == "JPEG":
        img.save(img_byte_arr, format='JPEG')
    elif format_type == "PDF":
        img.save(img_byte_arr, format='PDF')
    img_byte_arr.seek(0)
    return img_byte_arr

# Layout Streamlit
st.title("Image Rotator")
st.write("Upload Gambar untuk Merotasi by.triokacamata.")

# Upload gambar
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Load image
    img = load_image(uploaded_file)
    st.image(img, caption="Original Image", use_container_width=True)

    # Pengaturan rotasi
    rotation_angle = st.slider("Rotate Image", 0, 360, 0)
    img_rotated = rotate_image(img, rotation_angle)
    st.image(img_rotated, caption="Rotated Image", use_container_width=True)

    # Tombol download untuk setiap format
    st.write("Download the rotated image in your preferred format:")

    img_png = convert_image_to_bytes(img_rotated, "PNG")
    st.download_button(
        label="Download as PNG",
        data=img_png,
        file_name="rotated_image.png",
        mime="image/png"
    )

    img_jpeg = convert_image_to_bytes(img_rotated, "JPEG")
    st.download_button(
        label="Download as JPEG",
        data=img_jpeg,
        file_name="rotated_image.jpeg",
        mime="image/jpeg"
    )

    img_pdf = convert_image_to_bytes(img_rotated, "PDF")
    st.download_button(
        label="Download as PDF",
        data=img_pdf,
        file_name="rotated_image.pdf",
        mime="application/pdf"
    )