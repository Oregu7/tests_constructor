from django.conf.urls import url
from .views import test_list, test_category, test_detail, question_list, question_detail, user_detail
from .views import probationers_list, category_list, role_list, specialization_list, tested_list
urlpatterns = [
    url(r'^tests/$', test_list, name='test_list'),
    url(r'^tests/(?P<category>[A-Za-z]+)/$', test_category, name='test_category'),
    url(r'^tests/(?P<id>\d+)/$', test_detail, name='test_detail'),
    url(r'^tests/(?P<id>\d+)/questions/$', question_list, name="question_list"),
    url(r'^tests/(?P<test_id>\d+)/question/(?P<quest_id>\d+)/$', question_detail, name='question_detail'),
    url(r'^user/$', user_detail, name='user_detail'),
    url(r'^probationers/$', probationers_list, name='probationers_list'),
    url(r'^categories/$', category_list, name='category_list'),
    url(r'^rolies/$', role_list, name='role_list'),
    url(r'^specializations/$', specialization_list, name='specialization_list'),
    url(r'^testeds/$', tested_list, name='tested_list')
]
