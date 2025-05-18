import tensorflowjs as tfjs
from tensorflow.keras.models import load_model

# Load the model
model = load_model('covid_model.h5')

# Convert and save the model
tfjs.converters.save_keras_model(model, 'covidhelp/public/covid_model') 