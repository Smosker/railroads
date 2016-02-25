from django.conf.urls import url

from . import views

urlpatterns = [
    #example /shedule
    url(r'^$', views.index, name='index'),
    #example /shedule/train2/
    url(r'^train(?P<train_id>[0-9]+)/$', views.detail, name='detail'),
    #example /shedule/new-train/
    url(r'^new-train/$', views.new_train, name='new_train'),
    url(r'^new-train/result/$', views.result, name='result'),
    url(r'^weeks-schedule/$', views.weeks_schedule, name='weeks_schedule'),
    url(r'^select-route/$', views.select_route, name='select_route'),
    url(r'^select-route/change-data/$', views.change_data, name='change_data'),
    url(r'^select-route/change-data/change-results/$', views.change_results, name='change_results'),
    url(r'^weeks-schedule/view-routes/$', views.view_routes, name='view_routes'),
    url(r'^all-route/$', views.all_route, name='all_route'),

]
