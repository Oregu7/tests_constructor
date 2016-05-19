from django.http import QueryDict
from django.forms.models import model_to_dict
from django.contrib import auth
import json
import datetime

def check_sign_in(request):
    if request.user.is_authenticated():
        result = request.user
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
		item_data = model_to_dict(item)
		if 'date' in item_data:
			item_data['date'] = item_data['date'].strftime("%Y-%m-%d %H:%M:%S")
		result.append(item_data)
	return result

def get_number_name(number):
	if abs(number) < 12:
		if number == 3:
			result = 'three'
		elif number == 4:
			result = 'four'
		elif number == 5:
			result = 'five'
		elif number == 6:
			result = 'six'
		elif number == 7:
			result = 'seven'
		elif number == 8:
			result = 'eight'
		elif number == 9:
			result = 'nine'
		elif number == 10:
			result = 'teen'
		elif number == 11:
			result = 'eleven'
	else:
		result = 'twelve'
	return result