from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from testsConstructor.helpers import check_sign_in
from constructor.models import Test
from django.contrib import auth

# Create your views here.
def profile(request, login):
	user = check_sign_in(request)
	if user.username == login:
		tests = Test.objects.filter(creator=user)
		return render_to_response('profile.html', {'login': user, 'tests': tests})
	else:
		raise Http404('Это не ваш профиль : ' + login)