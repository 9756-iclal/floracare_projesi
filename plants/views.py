from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, CatalogPlant
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required(login_url='login')
def index(request):
    if request.method == 'POST':
        # 1. Durum: Kullanıcı el ile form doldurup bitki eklerse
        if 'manual_add' in request.POST:
            name = request.POST.get('name')
            soil_type = request.POST.get('soil_type')
            interval = request.POST.get('interval')

            Plant.objects.create(
                user=request.user,
                name=name,
                soil_type=soil_type,
                watering_interval_days=interval
            )
            return redirect('index')

        # 2. Durum: Kullanıcı katalogdan "Bitkilerime Ekle" butonuna basarsa
        elif 'catalog_add' in request.POST:
            catalog_id = request.POST.get('catalog_plant_id')
            catalog_plant = CatalogPlant.objects.get(id=catalog_id)

            # Katalogdaki hazır bilgileri kullanıcının kendi Plant listesine kopyalıyoruz
            Plant.objects.create(
                user=request.user,
                name=catalog_plant.name,
                soil_type=catalog_plant.soil_type,
                watering_interval_days=catalog_plant.watering_interval_days
            )
            return redirect('index')

    # Veritabanından verileri çekip HTML'e gönderiyoruz
    plants = Plant.objects.filter(user=request.user)
    catalog_plants = CatalogPlant.objects.all() # Katalogdaki tüm bitkileri çekiyoruz

    context = {
        'plants': plants,
        'catalog_plants': catalog_plants
    }
    return render(request, 'plants/index.html', context)

# === ÜYELİK FONKSİYONLARI ===
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'plants/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'plants/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('login')

# === HIZLI STOK / SATIŞ FONKSİYONU ===
@require_POST
def sell_plant(request, plant_id):
    plant = get_object_or_404(CatalogPlant, id=plant_id)
    if plant.stock > 0:
        plant.stock -= 1
        plant.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))