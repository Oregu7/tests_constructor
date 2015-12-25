from django.shortcuts import render_to_response
from constructor.models import Test, Query, Answer
from testsConstructor.helpers import check_sign_in
# Create your views here.
def tests(request):
	login = check_sign_in(request)
	test = Test.objects.all()
	return render_to_response('tests.html', {'tests': test, 'login': login})