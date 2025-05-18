from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import requests
import tempfile
import zipfile

def combine_model_parts(parts_dir, output_path):
    """Combine split model parts into a single file"""
    if not os.path.exists(output_path):
        # Get all parts sorted by number
        parts = sorted([f for f in os.listdir(parts_dir) if f.startswith('covid_model.part')])
        
        # Combine parts
        with open(output_path, 'wb') as outfile:
            for part in parts:
                part_path = os.path.join(parts_dir, part)
                with open(part_path, 'rb') as infile:
                    outfile.write(infile.read())

# Create temp directory for model
MODEL_DIR = os.path.join(tempfile.gettempdir(), 'covid_model')
os.makedirs(MODEL_DIR, exist_ok=True)

# Load model only once when the module is loaded
try:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(MODEL_DIR, 'covid_model.h5')
    combine_model_parts(base_dir, model_path)
    model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def home(request):
    return render(request, 'detector/home.html')

def detect(request):
    global model
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            if model is None:
                # Try to load model again if it failed initially
                try:
                    base_dir = os.path.dirname(os.path.dirname(__file__))
                    model_path = os.path.join(MODEL_DIR, 'covid_model.h5')
                    combine_model_parts(base_dir, model_path)
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

def health_check(request):
    return HttpResponse("OK", content_type="text/plain")
