from keras.preprocessing.image import ImageDataGenerator
import config

def get_data_generators():
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,  # Increased rotation range
        width_shift_range=0.3,  # Increased width shift range
        height_shift_range=0.3,  # Increased height shift range
        shear_range=0.3,  # Increased shear range
        zoom_range=0.3,  # Increased zoom range
        horizontal_flip=True,
        fill_mode="nearest",
        validation_split=0.2  # Chia 20% dữ liệu train thành validation
    )

    train_generator = train_datagen.flow_from_directory(
        config.TRAIN_DIR,
        target_size=config.IMG_SIZE,  # Sửa thành config.IMG_SIZE để đồng nhất
        batch_size=config.BATCH_SIZE,
        class_mode="categorical",
        subset="training",
        shuffle=True
    )

    val_generator = train_datagen.flow_from_directory(
        config.TRAIN_DIR,
        target_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode="categorical",
        subset="validation",
        shuffle=True
    )

    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        config.TEST_DIR,
        target_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode="categorical",
        shuffle=False
    )

    return train_generator, val_generator, test_generator

if __name__ == "__main__":
    train_gen, val_gen, test_gen = get_data_generators()
    print("✅ Dữ liệu đã được tạo thành công!")
    print(f"📂 Số lớp: {len(train_gen.class_indices)}")
    print(f"📸 Số ảnh train: {train_gen.samples}")
    print(f"📸 Số ảnh validation: {val_gen.samples}")
    print(f"📸 Số ảnh test: {test_gen.samples}")