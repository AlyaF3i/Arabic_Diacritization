import tensorflow as tf
import keras
import torch

class Sequential_Diacritizer():

    def init(self):
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Embedding(60, 8, input_length=125))
        self.model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM( 64, return_sequences=True)))
        self.model.add(tf.keras.layers.BatchNormalization())
        self.model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(192, return_sequences=True)))
        self.model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(192, return_sequences=True)))
        self.model.add(tf.keras.layers.Dense(16, activation='softmax'))
        self.model.compile(optimizer = 'adam', #rmsprop
                      loss = 'categorical_crossentropy', #sparse_
                      metrics =['accuracy'])

    def train(self, X, Y):
        self.model.fit(X,
              Y,
              batch_size=2,
              epochs=58,
              verbose=1,
              validation_split = 0.05,
              initial_epoch=0,
              )

         torch.save(model, '/content/drive/MyDrive/Seq/model.pt')
