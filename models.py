import os
import cv2
import numpy as np
import zipfile
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split


def extract_zip(zip_path, extract_to):
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(extract_to)
        print(f"Extracted to {extract_to}")
        return True
    except zipfile.BadZipFile:
        print("ERROR: Invalid zip file. Please redownload the dataset.")
        return False

def load_images(folder_path, label, img_size=(100, 100)):

    images = []
    labels = []
    if not os.path.exists(folder_path):
        print(f"Warning: Directory not found - {folder_path}")
        return np.array(images), np.array(labels)
        
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        try:
            img = cv2.imread(img_path)
            if img is None:
                raise ValueError("Failed to read image")
            img = cv2.resize(img, img_size)
            img = img / 255.0  # Normalize
            images.append(img)
            labels.append(label)
        except Exception as e:
            print(f"Skipping {filename}: {str(e)}")
    return np.array(images), np.array(labels)

def create_model(input_shape=(100, 100, 3)):
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=input_shape),
        MaxPool2D((2,2)),
        Conv2D(64, (3,3), activation='relu'),
        MaxPool2D((2,2)),
        Conv2D(128, (3,3), activation='relu'),
        MaxPool2D((2,2)),
        Flatten(),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.3),
        Dense(128, activation='relu'),
        Dense(3, activation='softmax')
    ])
    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


if __name__ == "__main__":
 
    DATASET_ROOT = os.path.join("covid_dataset", "Covid19-dataset")
    MODEL_PATH = "covid_model.h5"
    
  
    print("\nChecking dataset structure...")
    required_folders = [
        os.path.join(DATASET_ROOT, "train", "Covid"),
        os.path.join(DATASET_ROOT, "train", "Normal"),
        os.path.join(DATASET_ROOT, "train", "Viral Pneumonia"),
        os.path.join(DATASET_ROOT, "test", "Covid"),
        os.path.join(DATASET_ROOT, "test", "Normal"),
        os.path.join(DATASET_ROOT, "test", "Viral Pneumonia")
    ]
    
    missing = [folder for folder in required_folders if not os.path.exists(folder)]

  
    print("\nLoading dataset...")
    train_dir = os.path.join(DATASET_ROOT, "train")
    test_dir = os.path.join(DATASET_ROOT, "test")
    
 
    covid_train, covid_labels = load_images(os.path.join(train_dir, "Covid"), 0)
    normal_train, normal_labels = load_images(os.path.join(train_dir, "Normal"), 1)
    pneumonia_train, pneumonia_labels = load_images(os.path.join(train_dir, "Viral Pneumonia"), 2)
    
  
    X_train = np.concatenate((covid_train, normal_train, pneumonia_train))
    y_train = np.concatenate((covid_labels, normal_labels, pneumonia_labels))
    

    print("\nTraining model...")
    model = create_model()
    model.summary()
    
 
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
    
    history = model.fit(X_train, y_train,
                        validation_data=(X_val, y_val),
                        epochs=30,
                        batch_size=16)
    
 
    model.save(MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")

    
    print("\nEvaluating on test set...")
    covid_test, _ = load_images(os.path.join(test_dir, "Covid"), 0)
    normal_test, _ = load_images(os.path.join(test_dir, "Normal"), 1)
    pneumonia_test, _ = load_images(os.path.join(test_dir, "Viral Pneumonia"), 2)
    
    X_test = np.concatenate((covid_test, normal_test, pneumonia_test))
    y_test = np.concatenate((np.zeros(len(covid_test)), 
                            np.ones(len(normal_test)), 
                            np.full(len(pneumonia_test), 2)))
    
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {test_acc:.4f}")