from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # === YENİ ÜYELİK ADRESLERİ ===
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sell/<int:plant_id>/', views.sell_plant, name='sell_plant'),
]