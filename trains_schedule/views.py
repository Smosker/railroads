# coding=utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
import datetime
from trains_schedule.forms import RouteCreation
from trains_schedule.models import Schedule,City,Train



def check_time(departure_date, arriving_date):
    """
    Функция для проверки корректности ввода даты и времени
    Используется в views.WeeksSchedule
    """
    try:
        date_check1 = datetime.datetime.strptime(departure_date, '%Y-%m-%d %H:%M')
        date_check2 = datetime.datetime.strptime(arriving_date, '%Y-%m-%d %H:%M')
        if date_check1 >= date_check2:
                return HttpResponse("Error: date of arrival should be after date of departure")
    except ValueError:
            return HttpResponse("Error: you have to provide a valid date. "
                                "Return to the previous page and change the date input.")


class MainPage(View):
    """
    Отвечает за отображение информации на главной странице /shedule
    """
    model = Schedule
    train = Train
    template_name = 'trains_schedule/schedule.html'

    def get(self, request):
        time_now = timezone.now()
        time_after_week = time_now + datetime.timedelta(days=7)
        latest_schedule_list = self.model.objects.filter(departure_date__gte=time_now,
                                                         departure_date__lte=time_after_week).order_by('departure_date')
        context = {'latest_schedule_list': latest_schedule_list}
        if request.GET.get('search_value',None):
            trains = [route.id for route in self.model.objects.all()
                      if request.GET.get('search_value','').lower() in route.display_name().lower()]
            search_train_list = self.model.objects.filter(pk__in=trains)
            context['search_train_list'] = search_train_list
        return render(request, self.template_name, context)
'''
    def post(self,request):
        if request.GET['search_value']:
            trains = [route.id for route in self.model.objects.all()
                      if request.POST['search_value'].lower() in route.display_name().lower()]
            search_train_list = self.model.objects.filter(pk__in=trains)
            context = {'search_train_list': search_train_list}
            return render(request, self.template_name, context)
        else:
            return MainPage.get(self,request)

'''
class NewTrain(View):
    """
    Отвечает за вывод форм для ввода пользовтелем информации по новому маршруту
    на странице shedule/new-train/ при вводе корректной информации открывает
    карточку созданного маршрута
    """
    form_class = RouteCreation
    template_name = 'trains_schedule/new_train.html'

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class(initial={'departure_date': timezone.now().strftime('%Y-%m-%d %H:%M'),
                                        'destination_date': timezone.now().strftime('%Y-%m-%d %H:%M')})
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            route = form.save()
            return redirect('/schedule/trains/{}'.format(route.id))
        else:
            return HttpResponse("Error: you enter incorrect value. {}".format(form.errors))


class WeeksSchedule(View):
    """
    Отвечает за вывод форм для ввода пользовтелем информации о интересуемых
    датах маршрута и города(опционально) на странице shedule/weeks-schedule/
    и вывода соответствующей информации
    """
    model = Schedule
    city = City
    template_name = 'trains_schedule/weeks_shedule.html'

    def get(self, request):
        time_now = timezone.now().strftime("%Y-%m-%d %H:%M")
        context = {'time_now': time_now}
        return render(request, self.template_name, context)

    def post(self, request):
        date_from = request.POST['date_from'] if request.POST['date_from'] else '2000-01-01 00:00'
        date_to = request.POST['date_to'] if request.POST['date_to']else '8000-01-01 23:59'

        check = check_time(date_from, date_to)
        if check:
            return check

        schedule_list = self.model.objects.filter(departure_date__gte=date_from,
                                                  departure_date__lte=date_to).order_by('departure_date')

        context = {'schedule_list': schedule_list, 'date_from': request.POST['date_from'],
                   'date_to': request.POST['date_to']}

        if request.POST['city_from']:
            try:
                city = self.city.objects.get(city_name=request.POST['city_from'])
                schedule_list = schedule_list.filter(departure_city=city.id)
            except City.DoesNotExist:
                return HttpResponse("Error: you enter city name that is not in the base. "
                                    "Return to the previous page and enter another one")

            context['schedule_list'] = schedule_list
            context['city_from'] = request.POST['city_from']
        return render(request, self.template_name, context)


class AllRoutes(View):
    """
    Класс отвечающий за вывод информации о маршрутах,
    /schedule/trains/ - все маршруты
    /schedule/trains/19 - информация по конкретному маршруту
    Так же обрабатывает запросы на изменение/удаление маршрута
    """
    model = Schedule
    form_class = RouteCreation
    template_name = 'trains_schedule/trains.html'
    context_object_name = 'schedule_list'

    def get(self, request, train_id=None):
        if train_id:
            train = get_object_or_404(self.model, pk=train_id)
            context = {'train': train}
        else:
            context = {'schedule_list': self.model.objects.all().order_by('departure_date')}
        return render(request, self.template_name, context)

    def post(self, request, train_id):
        route = get_object_or_404(self.model, pk=train_id)

        if request.POST['action'] == 'Delete':
            return self.delete(route)

        elif request.POST['action'] == 'Save':
            form = self.form_class(request.POST, instance=route)
            if form.has_changed():
                if form.is_valid():
                    route = form.save()
                    return redirect('/schedule/trains/{}'.format(route.id))
                else:
                    return HttpResponse("Error: you enter incorrect value {}".format(form.errors))
            else:
                return HttpResponse("Error: you hadn't change anything")

        elif request.POST['action'] == 'Change':
            initial_data = {'departure_city': route.departure_city,
                            'destination_city': route.destination_city,
                            'departure_date':  route.departure_date.strftime('%Y-%m-%d %H:%M'),
                            'destination_date': route.destination_date.strftime('%Y-%m-%d %H:%M'),
                            'train': route.train}
            form = self.form_class(initial=initial_data)
            context = {'train': route, 'form': form}

            return render(request, self.template_name, context)

    def delete(self, route):
        """
        Отвечает за удаление переданного маршрута
        """
        response = u'Successful delete route {}'.format(route.display_name())
        route.delete()
        return HttpResponse(response)





