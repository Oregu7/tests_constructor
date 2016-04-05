from django.conf.urls import url, include
from .views import index, get_page, save_analytics
urlpatterns = [
    url(r'^$', index),
    url(r'^save/$', save_analytics),
    url(r'^(?P<page>\S+)/$', get_page)
]
