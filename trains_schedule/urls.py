from django.conf.urls import url
from . import views

urlpatterns = [
    #example /shedule
    url(r'^$', views.MainPage.as_view(), name='main'),
    url(r'^new-train/$', views.NewTrain.as_view(), name='new_train'),
    url(r'^weeks-schedule/$', views.WeeksSchedule.as_view(), name='weeks_schedule'),
    url(r'^trains/(?P<train_id>[0-9]+)?$', views.AllRoutes.as_view(), name='trains')
]
