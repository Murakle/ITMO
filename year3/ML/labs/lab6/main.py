import tensorflow as tf
import numpy as np
from mnist import MNIST
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # preapare data
    mnist_data = MNIST('data/mnist')
    mnist_train_images, mnist_train_labels = mnist_data.load_training()
    mnist_test_images, mnist_test_labels = mnist_data.load_testing()
    x_train = np.array(mnist_train_images)
    y_train = np.array(mnist_train_labels)
    x_test = np.array(mnist_test_images)
    y_test = np.array(mnist_test_labels)
    x_train, x_test = x_train / 255.0, x_test / 255.0
    x_train = tf.reshape(x_train, [60000, 28, 28, 1])
    x_test = tf.reshape(x_test, [10000, 28, 28, 1])

    # prepare model
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(6, 5, input_shape=(28, 28, 1)))  # 24 6
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))  # 12 6
    model.add(tf.keras.layers.Conv2D(16, (3, 3)))  # 10 16
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))  # 5 16
    model.add(tf.keras.layers.Conv2D(120, (5, 5)))  # 1 120
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(10))
    model.add(tf.keras.layers.Softmax())
    # model.add(tf.keras.layers.Maximum())

    model.summary()

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer='adam',
                  loss=loss_fn,
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0.9, 1])
    plt.legend(loc='lower right')
    plt.show()
    predicted = model.predict(x_test)
    result = [0] * len(predicted)
    most_similar = [] * 10
    for j in range(len(predicted)):
        res = predicted[j]
        for i in range(len(res)):
            if res[i] > res[result[j]]:
                result[j] = i
    cm = tf.math.confusion_matrix(y_test, result)
    print(cm)
