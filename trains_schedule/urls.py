from django.conf.urls import url
from . import views

urlpatterns = [
    #example /shedule
    url(r'^$', views.index, name='index'),
    #example /shedule/train2/
    url(r'^train(?P<train_id>[0-9]+)/$', views.detail, name='detail'),
    #example /shedule/new-train/
    url(r'^new-train/$', views.new_train, name='new_train'),
    url(r'^weeks-schedule/$', views.weeks_schedule, name='weeks_schedule'),
    url(r'^all-route/$', views.all_route, name='all_route'),

]
