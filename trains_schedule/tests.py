# coding=utf-8
from django.test import TestCase
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils import timezone
from trains_schedule.views import check_time
from trains_schedule.models import Schedule,City,Train



# Create your tests here.
class TimeCheckTests(TestCase):
    """
    Тесты для проверки работы функции views.check_time()
    """
    def test_check_time_positive(self):
        departure = '2016-01-01 12:00'
        arriving = '2016-01-02 13:12'
        self.assertEqual(check_time(departure, arriving), None)

    def test_check_time_negative(self):
        departure = '2016-01-02 12:00'
        arriving = '2015-01-02 13:12'
        response = HttpResponse("Error: date of arrival should be after date of departure")
        self.assertEqual(str(check_time(departure, arriving)), str(response))

        departure = arriving
        self.assertEqual(str(check_time(departure, arriving)), str(response))


class NewRouteTests(TestCase):
    """
    Тесты страницы /schedule/new-train

    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.city = City(city_name='test_city')
        self.city.save()
        self.train = Train(train_model='test_name', train_type='test',
                           train_type_description='test', train_capacity=20)
        self.train.save()


    def test_access(self):
        """
        Проверка на доступность без залогиневания
        """
        response = self.client.get(reverse('new_train'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('new_train'))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        """
        Проверка на ввод корректных/некорректных данных
        """
        self.client.login(username='testuser', password='testpass')
        data = {u'departure_date': [u'2016-04-08 15:06'], u'destination_date': [u'2016-04-11 15:06'],
                u'destination_city': [u'1'], u'train': [u'1'], u'departure_city': [u'1']}

        self.client.post(reverse('new_train'), data)
        print(Schedule.objects.all())
        self.assertEqual(len(Schedule.objects.all()), 1)

        data_wrong_date = {u'departure_date': [u'2016-04-15 15:06'], u'destination_date': [u'2016-04-11 15:06'],
                           u'destination_city': [u'1'], u'train': [u'1'], u'departure_city': [u'1']}

        self.client.post(reverse('new_train'), data_wrong_date)
        self.assertEqual(len(Schedule.objects.all()), 1)

        data_wrong_input = {u'departure_date': [u'2016-04-08 15:06 info'], u'destination_date': [u'2016-04-11 15:06'],
                            u'destination_city': [u'2'], u'train': [u'2'], u'departure_city': [u'1']}

        response = self.client.post(reverse('new_train'), data_wrong_input)
        self.assertEqual(len(Schedule.objects.all()), 1)
        self.assertEqual(response.content.startswith('Error: you enter incorrect value.'), True)


class AllRouteTests(TestCase):
    """
    Тесты страниц /schedule/trains  /schedule/trains/{{train_id}}

    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.city = City(city_name='test_city')
        self.city.save()
        self.train = Train(train_model='test_name', train_type='test',
                           train_type_description='test', train_capacity=20)
        self.train.save()
        self.route = Schedule(departure_date=timezone.now(), destination_date=timezone.now(),
                              destination_city=self.city, train=self.train, departure_city=self.city)
        self.route.save()


    def test_change(self):
        """
        Проверка на корректность обработки изменения данных
        """
        self.client.login(username='testuser', password='testpass')
        data_change_date_positive = {u'departure_date': [u'2010-03-22 17:11'], u'destination_date': [u'2010-03-22 20:00'],
                                     u'destination_city': [u'1'], u'train': [u'1'], u'departure_city': [u'1'], u'action': [u'Save']}

        self.client.post(reverse('trains', kwargs={'train_id': 1}), data_change_date_positive)
        self.assertEqual(str(Schedule.objects.get(pk=1).departure_date), '2010-03-22 17:11:00+00:00')

    def test_delete(self):
        """
        Проверка на корректность удаления
        """
        self.client.login(username='testuser', password='testpass')
        data_delete = {u'action': [u'Delete']}

        self.client.post(reverse('trains', kwargs={'train_id': 1}), data_delete)
        self.assertEqual(len(Schedule.objects.all()), 0)


class WeekScheduleTests(TestCase):
    """
    Тесты страниц /schedule/weeks-schedule/

    """
    def setUp(self):
        self.client = Client()
        self.city = City(city_name='test_city')
        self.city.save()
        self.train = Train(train_model='test_name', train_type='test',
                           train_type_description='test', train_capacity=20)
        self.train.save()
        self.route = Schedule(departure_date=timezone.now(), destination_date=timezone.now(),
                              destination_city=self.city, train=self.train, departure_city=self.city)
        self.route.save()

    def test_response(self):
        """
        Проверка на корректность обработки ввода неверной даты (пребытие раньше отъезда), города не из базы,
        неверной даты (вида '2016-04-09 11:55 info')
        """
        data = {u'city_from': [u'test_city'], u'date_from': [u'2016-04-12 11:55'],
                u'date_to': [u'2016-04-10 11:55']}
        response = self.client.post(reverse('weeks_schedule'), data)
        self.assertEqual(response.content, 'Error: date of arrival should be after date of departure')

        data = {u'city_from': [u'Wrong_city'], u'date_from': [u'2016-04-09 11:55'],
                u'date_to': [u'2016-04-10 11:55']}
        response = self.client.post(reverse('weeks_schedule'),data)
        self.assertEqual(response.content, 'Error: you enter city name that is not in the base. '
                                           'Return to the previous page and enter another one')

        data = {u'city_from': [u'test_city'], u'date_from': [u'2016-04-09 11:55 info'],
                u'date_to': [u'2016-04-10 11:55']}
        response = self.client.post(reverse('weeks_schedule'), data)
        self.assertEqual(response.content, 'Error: you have to provide a valid date. '
                                           'Return to the previous page and change the date input.')













