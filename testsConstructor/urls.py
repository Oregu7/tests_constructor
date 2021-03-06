"""testsConstructor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from testsConstructor.views import home, excel
from django.views import static
from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    url(r'^$', home),
    url(r'^excel/$', excel),
    url(r'^analytics/', include('analytics.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^profile/', include('users.urls')),
    url(r'^constructor/', include('constructor.urls')),
    url(r'^tests/', include('tests.urls')),
    url(r'^auth/', include('loginsys.urls'))
]

urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}))
