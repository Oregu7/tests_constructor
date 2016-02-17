from django.conf.urls import url

urlpatterns = [
    url(r'^tests/$', 'api.views.test_list', name='test_list'),
    url(r'^tests/(?P<category>[A-Za-z]+)/$', 'api.views.test_category', name='test_category'),
    url(r'^tests/(?P<id>\d+)/$', 'api.views.test_detail', name='test_detail'),
    url(r'^tests/(?P<id>\d+)/questions/$', 'api.views.question_list', name="question_list")
]
