import tensorflow as tf

def check_model():
    try:
        model = tf.keras.models.load_model('covid_model.h5')
        print("\nModel architecture:")
        model.summary()
        print("\nInput shape:", model.input_shape)
        print("Output shape:", model.output_shape)
    except Exception as e:
        print(f"Error loading model: {e}")

if __name__ == "__main__":
    check_model() 