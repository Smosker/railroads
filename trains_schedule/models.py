# coding=utf-8
from django.db import models


class City(models.Model):
    """
    Задает модель таблицы для базы данных городов
    """
    city_name = models.CharField(max_length=60)

    def trip_count(self):
        """
        Используется на форме администратора для отображения количества маршрутов в/из города
        """
        return self.s_departure_city_name.count() + self.s_destination_city_name.count()
    trip_count.short_description = 'Number of routes in/out of the city'

    def __unicode__(self):
        return u'{}'.format(self.city_name)




class Train(models.Model):
    """
    Задает модель таблицы для базы данных поездов
    """
    train_model = models.CharField(max_length=20)
    train_type = models.CharField(max_length=10)
    train_type_description = models.CharField(max_length=100)
    train_capacity = models.IntegerField(default=0)

    def __unicode__(self):
        return u'{} {}'.format(self.train_model, self.train_type)


class Schedule(models.Model):
    """
    Задает модель таблицы для базы данных о маршрутах
    """
    departure_city = models.ForeignKey(City, related_name='s_departure_city_name')
    destination_city = models.ForeignKey(City, related_name='s_destination_city_name')

    departure_date = models.DateTimeField('date of departure')
    destination_date = models.DateTimeField('date of arriving')

    train = models.ForeignKey(Train)

    def display_name(self):
        return u'{} from: {} {} to: {} {}'.format(self.train, self.departure_city,
                                                  self.departure_date.strftime("%Y-%m-%d %H:%M"),
                                                  self.destination_city,
                                                  self.destination_date.strftime("%Y-%m-%d %H:%M"))

    def display_train(self):
        return u'From: {} {}, To: {} {}'.format(self.departure_city, self.departure_date.strftime("%Y-%m-%d %H:%M"),
                                                self.destination_city, self.destination_date.strftime("%Y-%m-%d %H:%M"))

    def display_train_info(self):
        return u'Model: {}, Type: {}, Description: {}, Capacity: {}'.format(self.train.train_model,
                                                                            self.train.train_type,
                                                                            self.train.train_type_description,
                                                                            self.train.train_capacity)
