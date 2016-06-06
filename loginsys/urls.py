from django.conf.urls import url, include
from loginsys.views import login, logout, check, registration

urlpatterns = [
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^registration/$', registration),
    url(r'^check/$', check)
]