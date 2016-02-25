# coding=utf-8
from django.contrib import admin
from .models import Schedule,Train,City


class ScheduleAdmin(admin.ModelAdmin):
    """
    Управление таблицей с маршрутами
    """
    fieldsets = [
        (None,               {'fields': ['train']}),
        ('Departure', {'fields': ['departure_city', 'departure_date']}),
        ('Destination', {'fields': ['destination_city', 'destination_date']}),
    ]
    list_display = ('train', 'departure_city', 'departure_date', 'destination_city', 'destination_date')
    list_filter = ['departure_city', 'destination_city', 'departure_date', 'destination_date']
    search_fields = ['departure_city__city_name', 'destination_city__city_name']


class TrainAdmin(admin.ModelAdmin):
    """
    Управление таблицей с поездами
    """
    list_display = ('train_model', 'train_type', 'train_type_description', 'train_capacity')


class CityAdmin(admin.ModelAdmin):
    """
    Управление таблицей с городами
    """
    list_display = ('city_name','trip_count')
    search_fields = ['city_name']

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Train, TrainAdmin)
admin.site.register(City, CityAdmin)