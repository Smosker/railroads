from django.test import TestCase
from django.http import HttpResponse
from .views import check_time


# Create your tests here.
class TimeCheckTests(TestCase):
    def test_check_time_positive(self):
        departure = '2016-01-01 12:00:00'
        arriving = '2016-01-02 13:12:10'
        self.assertEqual(check_time(departure,arriving), None)

    def test_check_time_negative(self):
        departure = '2016-01-0 12:00:00'
        arriving = '0-01-02 13:12:10'
        response = HttpResponse("Error: you have to provide a valid date. "
                                "Return to the previous page and change the date input.")
        self.assertEqual(str(check_time(departure, arriving)), str(response))

        departure = '2016-01-02 12:00:00'
        arriving = '2015-01-02 13:12:10'
        response = HttpResponse("Error: date of arrival should be after date of departure")
        self.assertEqual(str(check_time(departure, arriving)), str(response))
