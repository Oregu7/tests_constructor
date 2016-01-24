from django.conf.urls import url, include
from constructor.views import *

urlpatterns = [
	url(r'^$', create_test),
	url(r'^test/(?P<id>\d+)/questions/$', queries_test),
	url(r'^test/(?P<id>\d+)/questions/add/$', add_query),
	url(r'^test/(?P<t_id>\d+)/questions/delete/(?P<q_id>\d+)/$', delete_query),
	url(r'^test/(?P<id>\d+)/settings/$', settings_test),
]