from .views import ProfileDetail, profile_update

from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<username>[\w-]+)/$', ProfileDetail.as_view(), name='detail'),
    url(r'^(?P<username>[\w-]+)/profile_update/$', profile_update, name='profile_update'),
]
