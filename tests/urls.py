from django.conf.urls import url, include
from tests.views import tests, get_page, test_detail

urlpatterns = [
    url(r'^$', tests),
    url(r'^(?P<id>\d+)/$', test_detail),
    url(r'^page/(?P<name>[a-zA-Z]+)/$', get_page)

]