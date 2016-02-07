from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from testsConstructor.helpers import check_sign_in, models_to_dict
from constructor.models import Test
from tests.models import Probationer
from django.contrib import auth
import json

# Create your views here.
def profile(request, login):
	user = check_sign_in(request)
	if user.username == login:
		tests = Test.objects.filter(creator=user)
		return render_to_response('profile.html', {'login': user, 'tests': tests})
	else:
		raise Http404('Это не ваш профиль : ' + login)

def test_results(request, login, id):
	user = check_sign_in(request)
	test = get_object_or_404(Test,id=id, creator=user)
	if request.is_ajax():
		probationers = models_to_dict(Probationer.objects.filter(test=test).order_by('-date'))
		return HttpResponse(json.dumps(probationers))
	else:
		return render_to_response('test_results.html', {'login': user, 'test': test})