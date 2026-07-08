from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Bitki Adı")
    soil_type = models.CharField(max_length=100, verbose_name="Toprak Türü")
    watering_interval_days = models.IntegerField(verbose_name="Kaç Günde Bir Sulanmalı?")
    last_watered_date = models.DateField(default=timezone.now, verbose_name="Son Sulama Tarihi")

    # Sulama zamanının gelip gelmediğini hesaplayan fonksiyon
    @property
    def needs_watering(self):
        next_watering_date = self.last_watered_date + timedelta(days=self.watering_interval_days)
        return timezone.now().date() >= next_watering_date

    def __str__(self):
        return self.name


class CatalogPlant(models.Model):
    name = models.CharField(max_length=100, verbose_name="Bitki Adı")
    soil_type = models.CharField(max_length=100, verbose_name="İdeal Toprak Türü")
    watering_interval_days = models.IntegerField(verbose_name="Varsayılan Sulama Sıklığı (Gün)")
    image_url = models.URLField(max_length=500, verbose_name="Bitki Resim URL'i", blank=True, null=True)
    description = models.TextField(verbose_name="Bitki Hakkında Bilgi / Bakım Tüyoları", blank=True, null=True)

    def __str__(self):
        return self.name