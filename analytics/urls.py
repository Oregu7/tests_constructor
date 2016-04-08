from django.conf.urls import url, include
from .views import index, get_page, save_analytics, send_to_excel, search_and_send_to_excel
urlpatterns = [
    url(r'^$', index),
    url(r'^save/$', save_analytics),
    url(r'^(?P<data>\w+)/(?P<test>\d+)/$', send_to_excel),
    url(r'^questions/test/(?P<test>\d+)/role/(?P<role>\d*)/spec/(?P<spec>\d*)/course/(?P<course>\d*)/date_f/(?P<date_f>\S*)/date_l/(?P<date_l>\S*)/$', search_and_send_to_excel),
    url(r'^(?P<page>\S+)/$', get_page)

]
