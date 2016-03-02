# coding=utf-8
from django.test import TestCase
from django.http import HttpResponse
from .views import check_time


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
