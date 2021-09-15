import numpy
import os
import sys
import tensorflow as tf

batch_size = 32
height = 365 // 2
width = 492 // 2
seed = 314159
split = 0.2
epoch_size = int(sys.argv[3])
overtrain_patience = 4
learn_rate = 1e-05

os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.4/bin") 
os.environ["TF_GPU_ALLOCATOR"] = "cuda_malloc_async"

print("TensorFlow version: {}".format(tf.__version__))

try:
    dir = str(sys.argv[1])
except (IndexError, FileNotFoundError):
    print("Error: cannot find given training data path")
    sys.exit(1)

#load training data
train = tf.keras.preprocessing.image_dataset_from_directory(
    dir,
    color_mode = 'grayscale',
    validation_split = split,
    subset = "training",
    seed = seed,
    image_size = (height, width),
    batch_size = batch_size,
    shuffle = True
)

val = tf.keras.preprocessing.image_dataset_from_directory(
    dir,
    color_mode = 'grayscale',
    validation_split = split,
    subset = "validation",
    seed = seed,
    image_size = (height, width),
    batch_size = batch_size,
    shuffle = True
)  

names = train.class_names

print("Training classes: {}".format(names))

#cache training data
train = train.prefetch(buffer_size = tf.data.experimental.AUTOTUNE)
val = val.prefetch(buffer_size = tf.data.experimental.AUTOTUNE)

#create model
class_size = len(names)

model = tf.keras.Sequential([
    tf.keras.layers.experimental.preprocessing.Rescaling(1./255, input_shape = (height, width, 1)),
    tf.keras.layers.Conv2D(4, kernel_size = (3,3), activation = 'relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(8, kernel_size = (3,3), activation = 'relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(16, kernel_size = (3,3), activation = 'relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(32, kernel_size = (3,3), activation = 'relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32, activation = 'relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(class_size)
])

opt = tf.keras.optimizers.Adam(learning_rate = learn_rate)

model.compile(optimizer=opt,
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'])

model.summary()

stoptraining = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience = overtrain_patience)
savemodel = tf.keras.callbacks.ModelCheckpoint(filepath = sys.argv[2], monitor = 'val_loss', verbose = 1, save_best_only = True, mode = 'min')

history = model.fit(
    train,
    batch_size = batch_size,
    validation_data = val,
    epochs = epoch_size,
    callbacks = [stoptraining, savemodel],
    shuffle = True
)