from django.conf.urls import url, include
from users.views import profile, test_results, test_analytic, get_page

urlpatterns = [
    url(r'^$', profile),
    url(r'^page/(?P<name>[A-Za-z]+)/$', get_page),
    url(r'^results/(?P<id>\d+)/$', test_results),
    url(r'^analytics/(?P<id>\d+)/$', test_analytic)
]