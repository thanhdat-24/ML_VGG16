import tensorflow as tf
from keras.models import Model
from keras.layers import Dense, Dropout, BatchNormalization, GlobalAveragePooling2D, Activation
from keras.applications import VGG16
import config

def build_vgg16():
    base_model = VGG16(weights="imagenet", include_top=False, input_shape=config.IMG_SIZE + (3,))
    
    # Đóng băng toàn bộ base model
    base_model.trainable = False

    # Thêm lớp mới
    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(512)(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(config.NUM_CLASSES, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=x)
    return model, base_model

def fine_tune_model(model, base_model, num_layers=4, lr=1e-5):
    # Mở khóa 4 layer cuối cùng của base model
    for layer in base_model.layers[-num_layers:]:
        layer.trainable = True

    # Compile lại với learning rate thấp
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
                  loss="categorical_crossentropy", 
                  metrics=["accuracy"])
    return model