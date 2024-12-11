import streamlit as st
from PIL import Image, ImageEnhance
import io

# Nama Kelompok
st.markdown("### Kelompok: Bagus Eric Kurniawan, Muchammad Ilham Bintang, Muhammad Rafi Fauzan")

# Fungsi untuk memuat gambar
def load_image(image_file):
    img = Image.open(image_file)
    return img

# Fungsi untuk merotasi gambar
def rotate_image(img, angle):
    return img.rotate(angle, expand=True)

# Fungsi untuk mengatur kecerahan gambar
def adjust_brightness(img, factor):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

# Fungsi untuk memperbesar atau memperkecil gambar
def scale_image(img, scale_factor):
    width, height = img.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return img.resize((new_width, new_height))

# Fungsi untuk mengubah orientasi gambar menjadi potret atau lanskap
def change_orientation(img, orientation):
    if orientation == "Potret" and img.width > img.height:
        return img.rotate(90, expand=True)
    elif orientation == "Lanskap" and img.height > img.width:
        return img.rotate(90, expand=True)
    return img

# Fungsi untuk mengubah intensitas warna RGB
def adjust_rgb(img, red_factor, green_factor, blue_factor):
    r, g, b = img.split()
    r = r.point(lambda i: i * red_factor)
    g = g.point(lambda i: i * green_factor)
    b = b.point(lambda i: i * blue_factor)
    return Image.merge("RGB", (r, g, b))

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
st.title("Editor Gambar")
st.write("Unggah gambar dan edit dengan orientasi, rotasi, skala, kecerahan, dan pengaturan RGB.")

# Upload gambar
uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Load image
    img = load_image(uploaded_file)
    st.image(img, caption="Gambar Asli", use_container_width=True)

    # Pengaturan orientasi
    orientation = st.radio("Ubah Orientasi", ("Asli", "Potret", "Lanskap"))
    img_oriented = change_orientation(img, orientation) if orientation != "Asli" else img
    st.image(img_oriented, caption="Hasil Setelah Mengubah Orientasi", use_container_width=True)

    # Pilihan mode rotasi
    rotation_mode = st.radio("Mode Rotasi", ("Manual", "Otomatis"))

    if rotation_mode == "Manual":
        # Pengaturan rotasi manual
        manual_rotation = st.slider("Rotasi Manual (0-360°)", 0, 360, 0)
        img_rotated = rotate_image(img_oriented, manual_rotation)
    else:
        # Pengaturan rotasi otomatis
        auto_rotation = st.selectbox("Rotasi Otomatis", [0, 45, 90, 135, 180, 225, 270, 315, 360])
        img_rotated = rotate_image(img_oriented, auto_rotation)

    # Pengaturan kecerahan
    brightness_factor = st.slider("Atur Kecerahan", 0.1, 2.0, 1.0)
    img_bright = adjust_brightness(img_rotated, brightness_factor)

    # Pengaturan skala
    scale_factor = st.slider("Ubah Skala Gambar", 0.1, 3.0, 1.0)
    img_scaled = scale_image(img_bright, scale_factor)

    # Pengaturan RGB
    st.write("Atur Intensitas RGB:")
    red_factor = st.slider("Intensitas Merah", 0.0, 2.0, 1.0)
    green_factor = st.slider("Intensitas Hijau", 0.0, 2.0, 1.0)
    blue_factor = st.slider("Intensitas Biru", 0.0, 2.0, 1.0)
    img_rgb = adjust_rgb(img_scaled, red_factor, green_factor, blue_factor)

    st.image(img_rgb, caption="Gambar Setelah Diedit", use_container_width=True)

    # Tombol download untuk setiap format
    st.write("Unduh gambar yang telah diedit dalam format pilihan Anda:")

    img_png = convert_image_to_bytes(img_rgb, "PNG")
    st.download_button(
        label="Unduh sebagai PNG",
        data=img_png,
        file_name="gambar_diedit.png",
        mime="image/png"
    )

    img_jpeg = convert_image_to_bytes(img_rgb, "JPEG")
    st.download_button(
        label="Unduh sebagai JPEG",
        data=img_jpeg,
        file_name="gambar_diedit.jpeg",
        mime="image/jpeg"
    )

    img_pdf = convert_image_to_bytes(img_rgb, "PDF")
    st.download_button(
        label="Unduh sebagai PDF",
        data=img_pdf,
        file_name="gambar_diedit.pdf",
        mime="application/pdf"
    )
