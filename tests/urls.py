from django.conf.urls import url, include
from tests.views import tests
urlpatterns = [
	url(r'^$', tests)
]