import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# data loading
df_input = pd.read_csv("input_DSCOV.csv")
df_output = pd.read_csv("output_Kp.csv")

# preprocessing: discard rows with a NaN element in each dataset
df_input = df_input.dropna()
df_output = df_output.dropna()

# Concatenate data assuming they are aligned
merged_data = pd.concat([df_input, df_output], axis=1)

# input and output
x_data = merged_data.values[:, :53]  # take only the input data
y_data = merged_data.values[:, -1].reshape(-1, 1)  # take the last column as output

# defining other useful parameters
sequence_length = 60*60*72 
batch_size = 60*60*24 
train_split = int(0.8 * len(x_data)) 

# training dataset
dataset_train = keras.preprocessing.timeseries_dataset_from_array(
    x_data[:train_split],
    y_data[:train_split],
    sequence_length=sequence_length,
    sampling_rate=1,
    batch_size=batch_size,
)

# validation dataset
dataset_val = keras.preprocessing.timeseries_dataset_from_array(
    x_data[train_split:],
    y_data[train_split:],
    sequence_length=sequence_length,
    sampling_rate=1,
    batch_size=batch_size,
)

# model
inputs = keras.layers.Input(shape=(sequence_length, x_data.shape[1]))
lstm_out = keras.layers.LSTM(32)(inputs)
outputs = keras.layers.Dense(1)(lstm_out)

model = keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss="mse")
model.summary()

# callbacks
path_checkpoint = "model_checkpoint.h5"
es_callback = keras.callbacks.EarlyStopping(monitor="val_loss", min_delta=0, patience=5)

modelckpt_callback = keras.callbacks.ModelCheckpoint(
    monitor="val_loss",
    filepath=path_checkpoint,
    verbose=1,
    save_weights_only=True,
    save_best_only=True,
)

# training
history = model.fit(
    dataset_train,
    epochs=100,
    validation_data=dataset_val,
    callbacks=[es_callback, modelckpt_callback],
)

# visualizing the loss
def visualize_loss(history, title):
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]
    epochs = range(len(loss))
    plt.figure()
    plt.plot(epochs, loss, "b", label="Training loss")
    plt.plot(epochs, val_loss, "r", label="Validation loss")
    plt.title(title)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()

visualize_loss(history, "Training and Validation Loss")
