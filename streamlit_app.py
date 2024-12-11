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
    img_byte_arr.seek(0)
    return img_byte_arr

# Layout Streamlit
st.title("Image Rotator")
st.write("Upload an image and rotate it to your desired angle.")

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

    # Pilihan format gambar untuk diunduh
    format_type = st.selectbox("Choose image format to download", ["PNG", "JPEG"])

    # Konversi gambar yang sudah dirotasi menjadi format byte untuk download
    img_for_download = convert_image_to_bytes(img_rotated, format_type)

    # Tombol download
    st.download_button(
        label=f"Download Image as {format_type}",
        data=img_for_download,
        file_name=f"rotated_image.{format_type.lower()}",
        mime=f"image/{format_type.lower()}"
    )
