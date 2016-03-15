# coding=utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import datetime
from .forms import RouteCreation
from .models import Schedule, City
from rest_framework import viewsets
from rest_framework import generics
from serializers import CitySerializer
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


def check_time(departure_date, arriving_date):
    """
    Функция для проверки корректности ввода даты и времени
    Используется в views.detail при изменении маршрута и
    в views.new_train при создании маршрута
    По заложенной функциональности дата отправления не должна быть больше даты прибытия
    """
    try:
        date_check1 = datetime.datetime.strptime(departure_date, '%Y-%m-%d %H:%M')
        date_check2 = datetime.datetime.strptime(arriving_date, '%Y-%m-%d %H:%M')
        if date_check1 > date_check2:
                return HttpResponse("Error: date of arrival should be after date of departure")
    except ValueError:
            return HttpResponse("Error: you have to provide a valid date. "
                                "Return to the previous page and change the date input.")


def index(request):
    """
    Отвечает за отображение информации на главной странице /shedule
    """
    latest_schedule_list = Schedule.objects.filter(departure_date__gte=timezone.now(),
                                                   departure_date__lte=timezone.now() +
                                                   datetime.timedelta(days=7)).order_by('departure_date')
    context = {'latest_schedule_list': latest_schedule_list}
    return render(request, 'trains_schedule/index.html', context)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def detail(request, train_id):
    """
    Отвечает за отображение информации по конкретному маршруту /shedule/train2/
    Так же дает возможность изменить или удалить маршрут.
    """
    route = get_object_or_404(Schedule, pk=train_id)
    if request.method == 'POST':

        if request.POST['action'] == 'Delete':
            response = u'Successful delete route {}'.format(route.display_name())
            route.delete()
            return HttpResponse(response)

        elif request.POST['action'] == 'Change':
            initial_data = {'departure_city': route.departure_city,
                            'destination_city': route.destination_city,
                            'departure_date':  route.departure_date.strftime('%Y-%m-%d %H:%M'),
                            'destination_date': route.destination_date.strftime('%Y-%m-%d %H:%M'),
                            'train': route.train}

            form = RouteCreation(initial=initial_data)
            context = {'train': route, 'form': form}

        elif request.POST['action'] == 'Save':
            form = RouteCreation(request.POST, instance=route)

            if form.is_valid():
                if check_time(request.POST['departure_date'], request.POST['destination_date']):
                    return check_time(request.POST['departure_date'], request.POST['destination_date'])
                route = form.save()
                return redirect('/schedule/train{}'.format(route.id))
            else:
                return HttpResponse("Error: you enter incorrect value")

    else:
        context = {'train': route}
    return render(request, 'trains_schedule/detail.html', context)

@login_required
def new_train(request):
    """
    Отвечает за вывод форм для ввода пользовтелем информации по новому маршруту
    на странице shedule/new-train/ при вводе корректной информации открывает
    карточку созданного маршрута
    """
    if request.method == 'POST':
        form = RouteCreation(request.POST)
        if form.is_valid():
            if check_time(request.POST['departure_date'], request.POST['destination_date']):
                return check_time(request.POST['departure_date'], request.POST['destination_date'])
            route = form.save()
            return redirect('/schedule/train{}'.format(route.id))
        else:
            return HttpResponse("Error: you enter incorrect value")

    else:
        form = RouteCreation(initial={'departure_date': timezone.now().strftime('%Y-%m-%d %H:%M'),
                                      'destination_date': timezone.now().strftime('%Y-%m-%d %H:%M')})
        context = {'form': form}
        return render(request, 'trains_schedule/new_train.html', context)


def weeks_schedule(request):
    """
    Отвечает за вывод форм для ввода пользовтелем информации о интересуемых
    датах маршрута и города(опционально) на странице shedule/weeks-schedule/
    и вывода соответствующей информации
    """
    if request.method == 'POST':
        date_from = request.POST['date_from'] if request.POST['date_from'] else '2000-01-01 00:00'
        date_to = request.POST['date_to'] if request.POST['date_to']else '8000-01-01 23:59'

        if check_time(date_from, date_to):
                return check_time(date_from, date_to)

        schedule_list = Schedule.objects.filter(departure_date__gte=date_from,
                                                departure_date__lte=date_to).order_by('departure_date')

        context = {'schedule_list': schedule_list, 'date_from': request.POST['date_from'],
                   'date_to': request.POST['date_to']}
        if request.POST['city_from']:
            try:
                city = City.objects.get(city_name=request.POST['city_from'])
                schedule_list = schedule_list.filter(departure_city=city.id)
            except City.DoesNotExist:
                return HttpResponse("Error: you enter city name that is not in the base. "
                                    "Return to the previous page and enter another one")
            context['schedule_list'] = schedule_list
            context['city_from'] = request.POST['city_from']

    else:
        time_now = timezone.now().strftime("%Y-%m-%d %H:%M")
        context = {'time_now': time_now}
    return render(request, 'trains_schedule/weeks_shedule.html', context)


def all_route(request):
    """
    Отвечает за вывод информации о всех маршрутах на странице schedule/all-route/
    Маршруты выводятся отсортированные по даты отправления
    """
    schedule_list = Schedule.objects.all().order_by('departure_date')
    context = {'schedule_list': schedule_list}
    return render(request, 'trains_schedule/schedule_all.html', context)