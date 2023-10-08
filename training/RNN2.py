import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# caricamento dati
df_input = pd.read_csv("input_DSCOV.csv")
df_output = pd.read_csv("output_Kp.csv")

# preprocessing: scarta da ogni dataset le righe che hanno un NaN come elemento
df_input = df_input.dropna()
df_output = df_output.dropna()

# Concatenazione dei dati assumendo che siano allineati
merged_data = pd.concat([df_input, df_output], axis=1)

# input e output
x_data = merged_data.values[:, :53]  # prendi solo i dati input
y_data = merged_data.values[:, -1].reshape(-1, 1)  # prendi l'ultima colonna come output

# definizione di altri parametri utili
sequence_length = 60*60*72 
batch_size = 60*60*24 
train_split = int(0.8 * len(x_data)) 

# dataset di training
dataset_train = keras.preprocessing.timeseries_dataset_from_array(
    x_data[:train_split],
    y_data[:train_split],
    sequence_length=sequence_length,
    sampling_rate=1,
    batch_size=batch_size,
)

# dataset di validazione
dataset_val = keras.preprocessing.timeseries_dataset_from_array(
    x_data[train_split:],
    y_data[train_split:],
    sequence_length=sequence_length,
    sampling_rate=1,
    batch_size=batch_size,
)

# modello
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

# visualizzazione della loss
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

