from django.conf.urls import url, include
from loginsys.views import * 

urlpatterns = [
	url(r'^login/$', login),
	url(r'^logout/$', logout),
	url(r'^check/$', check)
]