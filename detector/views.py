from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Load model only once when the module is loaded
try:
    model = tf.keras.models.load_model('covid_model.h5')
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def home(request):
    return render(request, 'detector/home.html')

def detect(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            if model is None:
                return JsonResponse({'error': 'Model not loaded'}, status=500)

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
