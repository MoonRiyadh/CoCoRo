import keras
from keras.layers import Convolution2D,Dense, MaxPooling2D, Dropout, Flatten
from keras.models import Sequential
from keras import optimizers
from keras.models import load_model
class Net:

    def __init__(self, input_shape):
        """
            input_shape is [number of samples per epoch, width, height]

            width and height refer to the dimensions of one sample.
            I.e, 250 samples --> width and 8 electrodes --> height
            One sample now has 8 rows and 250 columns

            number of epochs referes to the amount of samples used.
            I.e. if you have 250x8 matrix
        """
        self.input_shape = input_shape
        self. model = Sequential()


    def createCNN(self):
        """
        This creates a new CNN as specified in "Classification of Error Related Potentials using Convolutional Neural Networks" by Bellary et al.
        :return:None
        """
        self.model.add(Convolution2D(filters=16, kernel_size=(2,64), input_shape=self.input_shape))
        self.model.add(Convolution2D(filters=32, kernel_size=(1,64), activation='relu'))
        self.model.add(MaxPooling2D())
        self.model.add(Convolution2D(filters=32, kernel_size=(1,32), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=1))
        self.model.add(Convolution2D(filters=64, kernel_size=(1,16), activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(MaxPooling2D(pool_size=1))
        self.model.add(Flatten())
        self.model.add(Dense(2, activation='softmax'))
        custom_opt = optimizers.SGD(lr=0.001, momentum=0.9)
        self.model.compile(optimizer=custom_opt, loss='categorical_crossentropy', metrics= ['accuracy'])


    def fit(self, data, labels, epochs, batch_size=32, validation= None):
        """
        for model training, literally just calls keras.fit with our parameters on our model.
        :param batch_size: the amount of data and labels taken during one epoch
        :param data: training data
        :param labels: for each i in training data: label[i] = label(data[i])
        :param epochs: how long to train the model for
        :return: None
        """
        self.model.fit(data, labels, batch_size=batch_size, epochs=epochs, validation_split=validation)

    def save(self, path):
        self.model.save(path, overwrite=True)

    def load(self, path):
        self.model = load_model(path)

    def predict(self, data):
        return self.model.predict(data)

