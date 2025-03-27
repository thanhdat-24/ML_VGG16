from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import logging
import pyodbc
import base64
from config import IMG_SIZE, TRAIN_DIR, MODEL_SAVE_PATH

# Khởi tạo Flask, chỉ định thư mục chứa HTML và static files
app = Flask(__name__, 
            template_folder=os.path.abspath("frontend"),  # Thư mục chứa shop.html
            static_folder=os.path.abspath("frontend"))    # Chứa assets/css, assets/js

# Configure secret key for session management
app.secret_key = 'your_secret_key'

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Force TensorFlow to use the CPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Load mô hình đã train
model = tf.keras.models.load_model(MODEL_SAVE_PATH)

# Lấy danh sách lớp từ thư mục dataset
class_names = sorted([d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))])

# Database connection
def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=DESKTOP-CNH52PV\THANHDAT24;'
                          'DATABASE=QL_Fruit360;'
                          'UID=sa;PWD=123456')
    return conn

def preprocess_image(image):
    """ Tiền xử lý ảnh đầu vào trước khi đưa vào mô hình """
    image = image.convert("RGB")  # Chuyển ảnh RGBA hoặc Grayscale sang RGB
    image = image.resize((100, 100))  # Resize đúng với input của model
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)  # Thêm batch dimension
    return image

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TaiKhoan WHERE TaiKhoan = ? AND MatKhau = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session["user_id"] = user.ID_TK
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Tên người dùng hoặc mật khẩu không hợp lệ !")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route("/", methods=["GET"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Lấy thông tin tài khoản từ database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TaiKhoan, Avatar FROM TaiKhoan WHERE ID_TK = ?", (session["user_id"],))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return redirect(url_for("logout"))

    return render_template("indexTemplate.html", username=user.TaiKhoan, avatar_url=user.Avatar)

@app.route("/predict", methods=["POST"])
def predict():
    """ Xử lý ảnh tải lên và dự đoán loại hoa quả """
    if "file" not in request.files:
        app.logger.debug("No file part in the request")
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == '':
        app.logger.debug("No selected file")
        return jsonify({"error": "No file selected"}), 400

    try:
        image = Image.open(io.BytesIO(file.read()))
        processed_image = preprocess_image(image)

        # Chuyển ảnh thành base64 để hiển thị trên frontend
        img_io = io.BytesIO()
        image.save(img_io, format="PNG")
        img_base64 = "data:image/png;base64," + base64.b64encode(img_io.getvalue()).decode()

        # Dự đoán
        predictions = model.predict(processed_image)[0]
        top_5_indices = predictions.argsort()[-5:][::-1]  # Lấy 5 kết quả có xác suất cao nhất
        top_5_labels = [class_names[idx] for idx in top_5_indices]
        top_5_probs = [float(predictions[idx]) for idx in top_5_indices]

        app.logger.debug(f"Top 5 Predictions: {list(zip(top_5_labels, top_5_probs))}")

        return jsonify({
            "image": img_base64,  # Trả về ảnh dưới dạng base64
            "predictions": [{"label": label, "confidence": conf} for label, conf in zip(top_5_labels, top_5_probs)]
        })
    except Exception as e:
        app.logger.error(f"Error processing image: {e}")
        return jsonify({"error": "Error processing image"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)