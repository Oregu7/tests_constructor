from django.conf.urls import url

urlpatterns = [
    url(r'^tests/$', 'api.views.test_list', name='test_list'),
    url(r'^tests/(?P<category>[A-Za-z]+)/$', 'api.views.test_category', name='test_category'),
    url(r'^tests/(?P<id>\d+)/$', 'api.views.test_detail', name='test_detail'),
    url(r'^tests/(?P<id>\d+)/questions/$', 'api.views.question_list', name="question_list"),
    url(r'^tests/(?P<test_id>\d+)/question/(?P<quest_id>\d+)/$', 'api.views.question_detail', name='question_detail'),
    url(r'^user/$', 'api.views.user_detail', name='user_detail'),
    url(r'^probationers/$', 'api.views.probationers_list', name='probationers_list'),
    url(r'^categories/$', 'api.views.category_list', name='category_list'),
    url(r'^countries/$', 'api.views.country_list', name='country_list')
]
