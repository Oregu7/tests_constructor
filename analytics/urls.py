from django.conf.urls import url, include
from .views import index, get_page, save_analytics, send_to_excel
urlpatterns = [
    url(r'^$', index),
    url(r'^save/$', save_analytics),
    url(r'^(?P<page>\w+)/$', get_page),
    url(r'^(?P<data>\w+)/(?P<test>\d+)/$', send_to_excel)

]
