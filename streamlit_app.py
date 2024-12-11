import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import io

# Fungsi untuk memuat gambar
def load_image(image_file):
    img = Image.open(image_file)
    return img

# Fungsi untuk mengatur kecerahan gambar
def adjust_brightness(img, factor):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

# Fungsi untuk merotasi gambar
def rotate_image(img, angle):
    return img.rotate(angle)

# Fungsi untuk memperbesar atau memperkecil gambar
def zoom_image(img, zoom_factor):
    width, height = img.size
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)
    return img.resize((new_width, new_height))

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
st.title("Image Editor")
st.write("Upload an image to edit its brightness, rotate, or zoom.")

# Upload gambar
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Load image
    img = load_image(uploaded_file)
    st.image(img, caption="Original Image", use_container_width=True)
    
    # Pengaturan kecerahan
    brightness_factor = st.slider("Adjust Brightness", 0.1, 2.0, 1.0)
    img_bright = adjust_brightness(img, brightness_factor)
    st.image(img_bright, caption="Brightness Adjusted", use_container_width=True)
    
    # Pengaturan rotasi
    rotation_angle = st.slider("Rotate Image", 0, 360, 0)
    img_rotated = rotate_image(img_bright, rotation_angle)
    st.image(img_rotated, caption="Rotated Image", use_container_width=True)
    
    # Pengaturan Zoom
    zoom_factor = st.slider("Zoom In/Out", 0.1, 3.0, 1.0)
    img_zoomed = zoom_image(img_rotated, zoom_factor)
    st.image(img_zoomed, caption="Zoomed Image", use_container_width=True)
    
    # Pilihan format gambar untuk diunduh
    format_type = st.selectbox("Choose image format to download", ["PNG", "JPEG", "PDF"])
    
    # Konversi gambar yang sudah diubah menjadi format byte untuk download
    img_for_download = convert_image_to_bytes(img_zoomed, format_type)
    
    # Tombol download
    st.download_button(label=f"Download Image as {format_type}",
        data=img_for_download,
        file_name=f"edited_image.{format_type.lower()}",
        mime=f"image/{format_type.lower()}" if format_type != "PDF" else "application/pdf")