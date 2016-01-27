from django.conf.urls import url, include
from tests.views import *

urlpatterns = [
	url(r'^$', tests),
	url(r'^(?P<id>\d+)/$', test),
	url(r'^search/$', search)
]