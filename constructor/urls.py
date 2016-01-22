from django.conf.urls import url, include
from constructor.views import create_test, queries_test, add_query, delete_query, settings_test
urlpatterns = [
	url(r'^$', create_test),
	url(r'^test/(?P<id>\d+)/queries/$', queries_test),
	url(r'^test/(?P<id>\d+)/queries/add/$', add_query),
	url(r'^test/(?P<t_id>\d+)/queries/delete/(?P<q_id>\d+)/$', delete_query),
	url(r'^test/(?P<id>\d+)/settings/$', settings_test),
]