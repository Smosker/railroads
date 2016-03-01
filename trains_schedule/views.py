# coding=utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone

import datetime
from .forms import ChooseRoute, RouteCreation
from .models import Schedule, City, Train


def check_input(info):
    """
    Разбирает информацию полученную от пользователя для изменения/добавления маршрута
    """
    chosen_train = Train.objects.get(pk=info['choose_train'])
    chosen_departure_city = City.objects.get(pk=info['departure_city'])
    chosen_departure_time = '-'.join([info['departure_time_0_year'],
                                      info['departure_time_0_month'],
                                      info['departure_time_0_day']]) + ' ' + \
                            ':'.join([info['departure_time_1_hour'],
                                      info['departure_time_1_minute'],
                                      info['departure_time_1_second']])

    chosen_destination_city = City.objects.get(pk=info['destination_city'])

    chosen_arriving_time = '-'.join([info['arriving_time_0_year'],
                                     info['arriving_time_0_month'],
                                     info['arriving_time_0_day']]) + ' ' + \
                           ':'.join([info['arriving_time_1_hour'],
                                     info['arriving_time_1_minute'],
                                     info['arriving_time_1_second']])
    return chosen_train, chosen_departure_city, chosen_departure_time, \
           chosen_destination_city, chosen_arriving_time


def check_time(departure_date, arriving_date):
    """
    Функция выполняет проверку корректности данных о времени отправления и прибытия,
    введенных пользователем. Если данные не корректны возвращает соответствующую ошибку.
    """
    try:
        date_check1 = datetime.datetime.strptime(arriving_date, '%Y-%m-%d %H:%M:%S')
        date_check2 = datetime.datetime.strptime(departure_date, '%Y-%m-%d %H:%M:%S')
        if date_check1 <= date_check2:
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


def detail(request, train_id):
    """
    Отвечает за отображение информации по конкретному маршруту /shedule/train2/
    """
    route = get_object_or_404(Schedule, pk=train_id)
    if request.method == 'POST':

        if request.POST['action'] == 'Delete':
            response = 'Successful delete route {}'.format(route.display_name())
            route.delete()
            return HttpResponse(response)

        elif request.POST['action'] == 'Change':
            initial_data = {'departure_city': route.departure_city,
                            'destination_city': route.destination_city,
                            'departure_date':route.departure_date,
                            'destination_date':route.destination_date,
                            'train':route.train}

            form = RouteCreation(initial=initial_data)
            context = {'train': route, 'form': form}

        elif request.POST['action'] == 'Save':
            form = RouteCreation(request.POST, instance=route)
            if form.is_valid():
                route = form.save()
                return redirect('/schedule/train{}'.format(route.id))
            else:
                return HttpResponse("Error: you enter incorrect value")
    else:
        context = {'train': route}
    return render(request, 'trains_schedule/detail.html', context)


def new_train(request):
    """
    Отвечает за вывод форм для ввода пользовтелем информации по новому маршруту
    на странице shedule/new-train/
    """
    if request.method == 'POST':
        form = RouteCreation(request.POST)
        if form.is_valid():
            route = form.save()
            return redirect('/schedule/train{}'.format(route.id))
        else:
            return HttpResponse("Error: you enter incorrect value")

    else:
        form = RouteCreation(initial={'departure_date': '2016-03-01 12:43','destination_date': '2016-03-01 12:43'})
        context = {'form': form}
        return render(request, 'trains_schedule/new_train.html', context)


def weeks_schedule(request):
    """
    Отвечает за вывод форм для ввода пользовтелем информации о интересуемых
    датах маршрута и города(опционально) на странице shedule/weeks-schedule/
    передает информацию в schedule/weeks-schedule/view-routes/
    """
    if request.method == 'POST':
        date_from = request.POST['date_from'] if request.POST['date_from'] else '1700-01-01 00:00'
        date_to = request.POST['date_to'] if request.POST['date_to']else '8000-01-01 23:59'
        try:
            date_check1 = datetime.datetime.strptime(date_from, '%Y-%m-%d %H:%M')
            date_check2 = datetime.datetime.strptime(date_to, '%Y-%m-%d %H:%M')
            if date_check1 > date_check2:
                return HttpResponse("Error: date of arrival should be after date of departure")
        except ValueError:
            return HttpResponse("Error: you have to provide a valid date. "
                            "Return to the previous page and change the date input.")

        schedule_list = Schedule.objects.filter(departure_date__gte=date_from,
                                            departure_date__lte=date_to).order_by('departure_date')

        context = {'schedule_list': schedule_list, 'date_from':request.POST['date_from'], 'date_to':request.POST['date_to']}
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


def select_route(request):
    """
    Отвечает за вывод форм выбора маршрута для редактирования на странице
    schedule/select-route/, так же на форме есть возможно указать следует ли
    удалить маршрут, передает информацию /schedule/select-route/change-data/
    """
    available_choices = [(route.id, route.display_name()) for route in
                         Schedule.objects.all().order_by('departure_date')]
    if not available_choices:
        return HttpResponse("No route to display, you should add route first")
    form = ChooseRoute(choices=available_choices)
    context = {'form': form}
    return render(request, 'trains_schedule/select_route.html', context)


def change_data(request):
    """
    Отвечает за вывод формя для пользователя касательно внесения изменений в
    указанный на странице schedule/select-route/ маршрут, если delete_route == Y
    сразу удаляет маршрут и выводит соответствующее уведомление. Если delete_route != Y
    выведет форму для ввода новой информации по маршруту. Передает информацию в
    schedule/select-route/change-data/change-results
    """
    try:
        route = Schedule.objects.get(pk=request.POST['choose_route'])
        form = RouteCreation()
        context = {'route': route, 'form': form}
    except (KeyError, Schedule.DoesNotExist):
        return HttpResponse("Error: you didn't select a route. "
                            "Return to the previous page and choose one")

    if 'delete_route' in request.POST and request.POST['delete_route'] == 'Y':
        response = 'Successful delete route {}'.format(route.display_name())
        route.delete()
        return HttpResponse(response)

    return render(request, 'trains_schedule/change_data.html', context)


def change_results(request):
    """
    Обрабатывает информацию полученную со страницы schedule/select-route/change-data/
    Вывод ошибку в случае ввода неверной даты, если все данные введены верно -
    вносит изменения в маршрут выбранный на этапе schedule/select-route/,
    сохраняет данные и выводит соответствующее уведомление
    """

    chosen_train, chosen_departure_city, chosen_departure_time, \
    chosen_destination_city, chosen_arriving_time = check_input(request.POST)

    if check_time(chosen_departure_time, chosen_arriving_time):
        return check_time(chosen_departure_time, chosen_arriving_time)

    new_route = Schedule(id=request.POST['Route id'],
                         departure_city=chosen_departure_city,
                         destination_city=chosen_destination_city,
                         departure_date=chosen_departure_time,
                         destination_date=chosen_arriving_time,
                         train=chosen_train)
    new_route.save()
    response = "Successfully change the route"
    return HttpResponse(response)


def all_route(request):
    """
    Отвечает за вывод информации о всех маршрутах на странице schedule/all-route/
    Маршруты выводятся отсортированные по даты отправления
    """
    schedule_list = Schedule.objects.all().order_by('departure_date')
    context = {'schedule_list': schedule_list}
    return render(request, 'trains_schedule/schedule_all.html', context)