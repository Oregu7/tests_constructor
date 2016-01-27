from django.shortcuts import render_to_response, get_object_or_404, redirect
from testsConstructor.helpers import check_sign_in
from users.models import User
from constructor.models import Test
# Create your views here.
def profile(request, login):
	login = check_sign_in(request)
	user = get_object_or_404(User, login=login)
	if login == user.login:
		tests = Test.objects.filter(creator=user)
		return render_to_response('profile.html', {'login': login, 'tests': tests})
	else:
		return redirect('/')