from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Eksik olan ve hataya sebep olan satır buydu!
    path('', include('plants.urls')),
]