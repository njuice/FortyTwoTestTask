from django.conf.urls import patterns, url
from taskmng import views


urlpatterns = patterns(
    '',
    url(r'tasks/$', views.tasks, name='tasks'),
    url(r'current_user/', views.current_user, name='current_user'),
)
