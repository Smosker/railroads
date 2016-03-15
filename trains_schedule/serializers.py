from models import City,Schedule
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('id','city_name')

