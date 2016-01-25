from django.http import QueryDict
import json

def check_sign_in(request):
	if "user" in request.session:
		result = request.session.get('user')
	else:
		result = False
	return result

def str_to_bool(item):
	if item == "true":
		return True
	else:
		return False

def put(request):
	return json.loads(list(QueryDict(request.body).dict().keys())[0])