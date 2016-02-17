from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from testsConstructor.helpers import check_sign_in
def home(request):
	sign_in = check_sign_in(request)
	return render_to_response('home.html', {'login': sign_in})

