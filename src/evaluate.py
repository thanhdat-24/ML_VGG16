import tensorflow as tf
from data_preprocessing import get_data_generators
import config

# Load model
model = tf.keras.models.load_model(config.MODEL_SAVE_PATH)

# Load dữ liệu test
_, _, test_generator = get_data_generators()

# Đánh giá mô hình
loss, acc = model.evaluate(test_generator)
print(f"🎯 Độ chính xác trên tập test: {acc*100:.2f}%")