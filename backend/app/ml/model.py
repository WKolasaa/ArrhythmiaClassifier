import tensorflow as tf

CLASS_MAP = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4}  
NUM_CLASSES = len(CLASS_MAP)

def build_model(input_shape=(187, 1), num_classes=NUM_CLASSES):
    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.layers.Conv1D(32, kernel_size=5, activation='relu')(inputs)
    x = tf.keras.layers.MaxPool1D(2)(x)
    x = tf.keras.layers.Conv1D(64, kernel_size=5, activation='relu')(x)
    x = tf.keras.layers.MaxPool1D(2)(x)
    x = tf.keras.layers.LSTM(64)(x)
    x = tf.keras.layers.Dense(64, activation='relu')(x)
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)

    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model
