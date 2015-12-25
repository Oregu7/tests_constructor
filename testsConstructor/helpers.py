def check_sign_in(request):
	if "user" in request.session:
		result = request.session.get('user')
	else:
		result = False
	return result