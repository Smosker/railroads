from trains_schedule.models import Schedule, Train, City
from django.utils import timezone
from django.apps import registry

import django
django.setup()
'''#q = City(city_name='Helsinki')
#q.save()

q = Train(train_model='RZD-01',train_type='SV',
          train_type_description='description of train',
          train_capacity = 250
)
q.save()

q = Schedule(departure_date = timezone.now(),
             destination_date = timezone.now(),
             departure_city_id = 1,
             destination_city_id = 3,
             train_id = 1

)

q.save()

smosker
0880
'''

q = Schedule.objects.all()
print [str(s.train) for s in q]
'''
print q.departure_city
print q.destination_city
print q.display_name()
s = Train.objects.get(pk=1)
print s.schedule_set.all()

z = City.objects.get(pk=1)
print z.s_departure_city_name.all()
print z.s_destination_city_name.all()'''

avaluable_choices = [(route.id, route.display_name()) for route in Schedule.objects.all().order_by('departure_date')]
print avaluable_choices
