from django.conf.urls import url, include
from users.views import profile

urlpatterns = [
	url(r'(?P<login>\S+)/results/(?P<id>\d+)/$', 'users.views.test_results'),
    url(r'(?P<login>\S+)/analytics/(?P<id>\d+)/$', 'users.views.test_analytic'),
	url(r'(?P<login>\S+)/$', profile)
]