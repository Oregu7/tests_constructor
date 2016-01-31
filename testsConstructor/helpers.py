from django.http import QueryDict
from django.forms.models import model_to_dict
from django.contrib import auth
import json

def check_sign_in(request):
	if auth.get_user(request).username:
		result = auth.get_user(request).username
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

def models_to_dict(data):
	result = []
	for item in data:
		result.append(model_to_dict(item))
	return result