from django.shortcuts import render, redirect
from .models import Plant

def index(request):
    if request.method == 'POST':
        # HTML formundan gelen verileri yakalıyoruz
        name = request.POST.get('name')
        soil_type = request.POST.get('soil_type')
        interval = request.POST.get('interval')
        
        # Veritabanına yeni bitkiyi kaydediyoruz
        Plant.objects.create(
            name=name,
            soil_type=soil_type,
            watering_interval_days=interval
        )
        return redirect('index')

    # Veritabanındaki tüm bitkileri çekip HTML'e gönderiyoruz
    plants = Plant.objects.all()
    return render(request, 'plants/index.html', {'plants': plants})