from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from users.models import User
from testsConstructor.helpers import check_sign_in
def home(request):
	sign_in = check_sign_in(request)
	return render_to_response('home.html', {'login': sign_in})

def login(request):
	if request.is_ajax():
		try:
			user = User.objects.get(login=request.POST['login'], password = request.POST['password'])
			request.session['user'] = user.login
			response = JsonResponse({'error': False})
			if request.POST['remember'] == 'true':
				response.set_cookie('login', user.login, 36000)
			return response
		except ObjectDoesNotExist:
			return JsonResponse({'error': 'Неверный логин или пароль'})
	else:
		if 'user' in request.session:
			return redirect('/')
		else:
			return render_to_response('login.html')

def sign_out(request):
	response = redirect('/')
	if 'user' in request.session:
		del request.session['user']
	if 'login' in request.COOKIES:
		response.delete_cookie('login')
	return response