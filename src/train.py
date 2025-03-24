import tensorflow as tf
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from model import build_vgg16, fine_tune_model
from data_preprocessing import get_data_generators
import config

# Load dữ liệu
train_generator, val_generator, _ = get_data_generators()

# Xây dựng mô hình
model, base_model = build_vgg16()

# Compile mô hình ban đầu
model.compile(loss="categorical_crossentropy", optimizer=Adam(learning_rate=config.LEARNING_RATE), metrics=["accuracy"])

# Callback tránh overfitting
callbacks = [
    EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
    ReduceLROnPlateau(monitor="val_loss", factor=0.1, patience=3, verbose=1)
]

# Huấn luyện lần 1 (đóng băng base model)
print("🚀 Huấn luyện giai đoạn 1 (base model frozen)...")
model.fit(train_generator, validation_data=val_generator, epochs=config.EPOCHS, callbacks=callbacks)

# Fine-tune
print("\n🔥 Bắt đầu fine-tuning với 4 layer cuối của VGG16 mở khóa...")
model = fine_tune_model(model, base_model, num_layers=4, lr=1e-5)

# Huấn luyện lần 2 (fine-tune với learning rate thấp)
model.fit(train_generator, validation_data=val_generator, epochs=config.FINE_TUNE_EPOCHS, callbacks=callbacks)

# Lưu mô hình
model.save(config.MODEL_SAVE_PATH)
print(f"✅ Mô hình đã được lưu tại {config.MODEL_SAVE_PATH}")