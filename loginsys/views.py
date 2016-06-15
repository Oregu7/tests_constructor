from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib import auth
from testsConstructor.helpers import check_sign_in
from django.http import JsonResponse, HttpResponse, Http404, QueryDict
from users.models import Group, User
from users.serializers import GroupSerializer
from django.forms.models import model_to_dict
from django.core.context_processors import csrf
import json

# Create your views here.
def login(request):
    args = {
        'close_header': True
    }
    args.update(csrf(request))

    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('login', '').lower()
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return JsonResponse({'auth': True})
        else:
            return JsonResponse({'error': 'Не верный логин или пароль'})
    else:
        return render_to_response('login.html', args)

def logout(request):
    auth.logout(request)
    return redirect('/')

def check(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        action = data.get('action', '')
        if action == 'group':
            secret_key = data.get('secret_key', '')
            args = {}
            try:
                group = Group.objects.get(secret_key=secret_key)
                args['group'] = GroupSerializer(group).data
            except Group.DoesNotExist:
                args['group'] = False
                args['error'] = "Вы ввели неверный секретный код. Группа не найдена!"

            return JsonResponse(args)
        elif action == 'username':
            login = data.get('login', '').lower()
            try:
                user = User.objects.get(username=login)
                result = True
            except User.DoesNotExist:
                result = False
            return JsonResponse({'username': result})
        else:
            raise Http404('Действие не поддерживается!')
    else:
        raise Http404('Метод не поддерживается!')


def registration(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        #Регистрация пользователя
        user = User()
        user.username = data.get('login', '').lower()
        user.first_name = data.get('firstName', '').lower().title()
        user.last_name = data.get('lastName', '').lower().title()
        user.set_password(data.get('password', ''))
        user.study_group = get_object_or_404(Group, id=data.get('group', ''))
        user.save()
        #аутентификация
        user_auth = auth.authenticate(username=data.get('login', '').lower(), password=data.get('password', ''))
        if user_auth is not None:
            auth.login(request, user_auth)
        return JsonResponse({'registration': True})
    else:
        raise Http404('Метод не поддерживается!')