import os
# Đường dẫn dataset
DATASET_PATH = os.path.abspath("dataset")
TRAIN_DIR = os.path.join(DATASET_PATH, "Training")
TEST_DIR = os.path.join(DATASET_PATH, "Test")
# Đường dẫn lưu mô hình
MODEL_SAVE_PATH = os.path.abspath(os.path.join("saved_model", "vgg16_fruits360.h5"))
# Tham số huấn luyện
IMG_SIZE = (100, 100)  # Kích thước ảnh đầu vào
BATCH_SIZE = 64  # Kích thước batch
LEARNING_RATE = 1e-4  # Tốc độ học ban đầu
EPOCHS = 15  # Epochs đầu tiên (huấn luyện trên top layers)
FINE_TUNE_EPOCHS = 10  # Epochs fine-tune với các layer mở khóa
NUM_CLASSES = len([d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))])
CLASS_NAMES = sorted([d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))])