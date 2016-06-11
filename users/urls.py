from django.conf.urls import url, include
from users.views import profile, profile_data, test_results, test_analytic, get_page, tested_result, print_results

urlpatterns = [
    url(r'^$', profile),
    url(r'^data/$', profile_data),
    url(r'^page/(?P<name>[A-Za-z]+)/$', get_page),
    url(r'^results/(?P<id>\d+)/$', test_results),
    url(r'^print/results/(?P<id>\d+)/$', print_results),
    url(r'^tested/(?P<id>\d+)/$', tested_result),
    url(r'^analytics/(?P<id>\d+)/$', test_analytic)
]