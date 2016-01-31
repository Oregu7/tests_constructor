from django.conf.urls import url, include
from tests.views import *

urlpatterns = [
	url(r'^$', tests),
	url(r'^(?P<id>\d+)/$', test),
	url(r'^next/$', test_next_quest),
	url(r'^set_name/$', set_name),
	url(r'^search/$', search)
]