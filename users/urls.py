from django.conf.urls import url, include
from users.views import profile

urlpatterns = [
	url(r'(?P<login>\S+)/$', profile)
]