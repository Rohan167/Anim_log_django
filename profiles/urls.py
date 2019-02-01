from .views import ProfileDetail

from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<username>[\w-]+)/$', ProfileDetail.as_view(), name='detail'),
]
