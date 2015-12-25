from django.conf.urls import url, include
from constructor.views import create_test, settings_test
urlpatterns = [
	url(r'^$', create_test),
	url(r'^test/(?P<id>\d+)/$', settings_test)
]