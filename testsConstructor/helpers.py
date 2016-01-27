from django.http import QueryDict
from django.forms.models import model_to_dict
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

def models_to_dict(data):
	result = []
	for item in data:
		result.append(model_to_dict(item))
	return result