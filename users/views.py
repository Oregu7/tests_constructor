from django.shortcuts import render_to_response
from testsConstructor.helpers import check_sign_in
# Create your views here.
def profile(request, login):
	sign_in = check_sign_in(request)
	return render_to_response('profile.html', {'login': sign_in})