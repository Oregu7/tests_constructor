from django.conf.urls import url, include
from constructor.views import create_test, settings_test, add_query, delete_query
urlpatterns = [
	url(r'^$', create_test),
	url(r'^test/(?P<id>\d+)/$', settings_test),
	url(r'^test/(?P<id>\d+)/add/$', add_query),
	url(r'^test/(?P<t_id>\d+)/delete/(?P<q_id>\d+)/$', delete_query)
]