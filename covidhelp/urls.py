from django.contrib import admin
from django.urls import path, include
from detector.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),  # Add health check at root level
    path('', include('detector.urls')),  # Include detector URLs
] 