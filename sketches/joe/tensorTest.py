  import matplotlib.pyplot as plt
import tensorflow as tf

mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()


#plt.imshow(x_train[0], plt.cm.binary)
#plt.show()

print('(depth, row,col): (%d,%d,%d)' %  (len(x_train), len(x_train[0]), len(x_train[0][0])))

# Normalize data
x_train = tf.keras.utils.normalize(x_train)
x_test = tf.keras.utils.normalize(x_test)

####  creating model architcture  ####
model = tf.keras.models.Sequential() # creating model type -> sequential
# adding layers
model.add(tf.keras.layers.Flatten()) # this is the input layer which we are just using to flatten the tensor
model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu)) # one of the two hidden layers, using 'relu' as the activation fucntion
model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
model.add(tf.keras.layers.Dense(10,activation = tf.nn.softmax)) # output layer

#### feature specification ####
model.compile(optimizer = 'adam',
              loss = 'sparse_categorical_crossentropy',
              metrics = ['accuracy'])

#### training/fitting model #####
model.fit(x_train, y_train, epochs=3)

#### testing model #####
# loss and accuracy metrics let us know how our model is performing
valuation_loss, valuation_acc = model.evaluate(x_test, y_test)
print(valuation_loss, valuation_acc)


# model can be saved 
