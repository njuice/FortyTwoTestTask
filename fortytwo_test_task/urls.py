from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from taskmng.api.resources import *
admin.autodiscover()

api = Api(api_name='v1')
api.register(TasksResource())
api.register(UserResource())
api.register(UserSocialResource())

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.landing.urls', namespace="landing")),
    url(r'^', include('apps.taskmng.urls', namespace="taskmng")),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    (r'^api/', include(api.urls)),
)
