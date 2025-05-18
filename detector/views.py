from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import requests
import tempfile
import zipfile

def extract_model(zip_path, extract_dir):
    """Extract model from zip file if not already extracted"""
    model_path = os.path.join(extract_dir, 'covid_model.h5')
    if not os.path.exists(model_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    return model_path

# Create temp directory for model
MODEL_DIR = os.path.join(tempfile.gettempdir(), 'covid_model')
os.makedirs(MODEL_DIR, exist_ok=True)

# Load model only once when the module is loaded
try:
    zip_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'covid_model.zip')
    model_path = extract_model(zip_path, MODEL_DIR)
    model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def home(request):
    return render(request, 'detector/home.html')

def detect(request):
    global model  # Move global declaration to start of function
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            if model is None:
                # Try to load model again if it failed initially
                try:
                    zip_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'covid_model.zip')
                    model_path = extract_model(zip_path, MODEL_DIR)
                    model = tf.keras.models.load_model(model_path)
                except Exception as e:
                    return JsonResponse({'error': f'Could not load model: {str(e)}'}, status=500)

            # Read and preprocess image
            image_file = request.FILES['image']
            img = Image.open(image_file).convert('RGB')
            img = img.resize((100, 100))
            
            # Convert to numpy array with explicit shape
            img_array = np.asarray(img).astype(np.float32)
            img_array = img_array / 255.0
            img_array = img_array.reshape((1, 100, 100, 3))
            
            # Make prediction
            prediction = model.predict(img_array, verbose=0)
            pred_class = np.argmax(prediction[0])
            confidence = float(prediction[0][pred_class]) * 100
            
            result_map = {
                0: "COVID-19 Positive",
                1: "Normal (COVID-19 Negative)",
                2: "Viral Pneumonia"
            }
            
            return JsonResponse({
                'result': result_map[pred_class],
                'confidence': f"{confidence:.2f}%"
            })
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return JsonResponse({'error': str(e)}, status=400)
            
    return render(request, 'detector/detect.html')

def prevention(request):
    return render(request, 'detector/prevention.html')

def resources(request):
    return render(request, 'detector/resources.html')

def symptoms(request):
    return render(request, 'detector/symptoms.html')

def predict_image(request):
    if request.method == 'POST':
        MODEL_URL = os.environ.get('MODEL_URL', 'YOUR_GITHUB_RELEASE_URL_HERE')
        model_path = os.path.join(tempfile.gettempdir(), 'covid_model.h5')
        download_model(MODEL_URL, model_path)
        model = tf.keras.models.load_model(model_path)
        # ... rest of your code ...
