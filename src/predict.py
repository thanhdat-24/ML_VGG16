import tensorflow as tf
import numpy as np
import cv2
import config
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# Load mô hình đã train
model = tf.keras.models.load_model(config.MODEL_SAVE_PATH)

def predict_image(image_path):
    # Đọc ảnh và kiểm tra số kênh màu
    img = cv2.imread(image_path)
    if img is None:
        print("❌ Không thể đọc ảnh. Hãy kiểm tra lại đường dẫn!")
        return None, None, None

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Chuyển về RGB nếu cần
    img_resized = cv2.resize(img, tuple(config.IMG_SIZE))  # Resize ảnh về đúng kích thước huấn luyện

    # Chuyển đổi dtype chính xác
    img_array = img_resized / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Thêm batch dimension

    # Dự đoán
    predictions = model.predict(img_array)
    top_5_indices = predictions[0].argsort()[-5:][::-1]  # Lấy 5 kết quả có xác suất cao nhất
    top_5_probs = predictions[0][top_5_indices]

    # Lấy tên lớp từ chỉ số
    top_5_labels = [config.CLASS_NAMES[idx] for idx in top_5_indices]

    return img_resized, top_5_labels, top_5_probs

# Mở hộp thoại chọn ảnh nhiều lần
while True:
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Chọn ảnh để dự đoán")

    if not image_path:
        print("\n❌ Không có ảnh nào được chọn! Thoát chương trình.")
        break  # Thoát nếu người dùng nhấn "Hủy"

    img, top_5_labels, top_5_probs = predict_image(image_path)

    # Hiển thị ảnh
    plt.imshow(img)
    plt.axis("off")
    plt.title("Ảnh test")
    plt.show()

    # In kết quả dự đoán trên console
    print("\n🛑 Kết quả dự đoán (Top 5):")
    for i, (label, prob) in enumerate(zip(top_5_labels, top_5_probs), 1):
        print(f"{i}. {label} - Xác suất: {prob:.4f}")

    # Hỏi người dùng có muốn chọn ảnh khác không
    cont = input("\n🔄 Bạn có muốn chọn ảnh khác không? (y/n): ").strip().lower()
    if cont != "y":
        print("\n✅ Thoát chương trình.")
        break