import streamlit as st
from PIL import Image
import io

# Judul aplikasi
st.title("Rotating Picture App")

# Upload gambar
gupl = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if gupl is not None:
    # Membuka gambar yang diunggah
    img = Image.open(gupl)

    # Menampilkan gambar asli
    st.subheader("Original Image")
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Slider untuk menentukan rotasi
    rotation_angle = st.slider("Select Rotation Angle (degrees):", -360, 360, 0)

    # Memutar gambar
    rotated_img = img.rotate(rotation_angle, expand=True)

    # Menampilkan gambar yang telah diputar
    st.subheader("Rotated Image")
    st.image(rotated_img, caption=f"Image rotated by {rotation_angle} degrees", use_column_width=True)

    # Konversi gambar untuk format yang berbeda
    img_download = rotated_img.convert("RGB")
    img_bytes_jpg = io.BytesIO()
    img_bytes_png = io.BytesIO()
    img_bytes_pdf = io.BytesIO()

    img_download.save(img_bytes_jpg, format="JPEG")
    img_download.save(img_bytes_png, format="PNG")
    img_download.save(img_bytes_pdf, format="PDF")

    img_bytes_jpg.seek(0)
    img_bytes_png.seek(0)
    img_bytes_pdf.seek(0)

    # Tombol untuk mengunduh gambar yang telah diputar dalam format berbeda
    st.download_button(
        label="Download as JPEG",
        data=img_bytes_jpg,
        file_name="rotated_image.jpg",
        mime="image/jpeg"
    )

    st.download_button(
        label="Download as PNG",
        data=img_bytes_png,
        file_name="rotated_image.png",
        mime="image/png"
    )

    st.download_button(
        label="Download as PDF",
        data=img_bytes_pdf,
        file_name="rotated_image.pdf",
        mime="application/pdf"
    )
