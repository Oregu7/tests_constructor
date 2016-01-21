from django.conf.urls import url, include
from constructor.views import create_test, settings_test, add_query
urlpatterns = [
	url(r'^$', create_test),
	url(r'^test/(?P<id>\d+)/$', settings_test),
	url(r'^test/(?P<id>\d+)/add/$', add_query)
]