from django.conf.urls import url
from .views import (
                            anime_list_view,
                            anime_create_view,
                            anime_detail_view,
                            anime_createview_class,
                            anime_updateview_class
                        )

urlpatterns = [
    # url(r'^create/$', anime_createview_class.as_view(), name='create'),
    url(r'^create/$', anime_create_view, name='create'),
    url(r'^(?P<slug>[]\w-]+)/edit/$', anime_updateview_class.as_view(), name='edit'),
    url(r'^(?P<slug>[]\w-]+)/$', anime_detail_view.as_view(), name='detail'),
    url(r'$', anime_list_view.as_view(), name='list'),
]
