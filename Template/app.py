import streamlit as st
import tensorflow as tf
import numpy as np
import gdown
import os
from PIL import Image
import config

# Đường dẫn Google Drive (file ID từ link của bạn)
GDRIVE_MODEL_URL = "https://drive.google.com/uc?id=1OtNAPdyyb2Lf3jmHUVd3lYp5kA_gbSBZ"
MODEL_PATH = "vgg16_fruits360.h5"

# Tải model nếu chưa có
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):  # Kiểm tra nếu model chưa tồn tại
        st.info("Đang tải model, vui lòng chờ...")
        gdown.download(GDRIVE_MODEL_URL, MODEL_PATH, quiet=False)

    return tf.keras.models.load_model(MODEL_PATH)

# Load model
model = load_model()
class_labels = config.CLASS_NAMES  # Cập nhật danh sách lớp

# Hàm tiền xử lý ảnh
def preprocess_image(image):
    image = image.resize((100, 100))  # Resize ảnh về kích thước phù hợp
    image = np.array(image) / 255.0   # Chuẩn hóa pixel về [0,1]
    image = np.expand_dims(image, axis=0)  # Thêm batch dimension
    return image

# Giao diện Streamlit
st.title("Nhận diện hoa quả 🍎🍌🍊")
st.write("Tải ảnh hoa quả lên để hệ thống nhận diện loại quả và độ chính xác.")

uploaded_file = st.file_uploader("Chọn ảnh...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh đã tải lên", use_column_width=True)

    if st.button("Dự đoán"):
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        predicted_class = class_labels[np.argmax(predictions)]
        confidence = round(100 * np.max(predictions), 2)

        st.success(f"**Kết quả:** {predicted_class} 🍏")
        st.info(f"**Độ chính xác:** {confidence}%")