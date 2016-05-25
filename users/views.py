from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from testsConstructor.helpers import check_sign_in, models_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from constructor.models import Test, Option
from constructor.serializers import OptionSecondSerializer, OptionSerializer
from tests.models import Probationer
from tests.serializers import ProbationerSerializer
from .models import Group, Specialization
from .serializers import GroupSerializer, SpecializationSerializer
from django.contrib.auth.decorators import login_required
from rest_framework import status
import json

# Create your views here.
@login_required
def profile(request):
    user = request.user
    if user.is_staff:
        tests = Test.objects.filter(creator=user)
        return render_to_response('profile.html', {'login': user, 'tests': tests})
    else:
        raise Http404('Это не ваш профиль')

@login_required
def test_results(request, id):
    user = request.user
    test = get_object_or_404(Test,id=id, creator=user)
    data = {'login': user, 'test': test}
    data.update(csrf(request))
    if request.is_ajax():
        if request.method == "GET":
            specializations = SpecializationSerializer(Specialization.objects.all(), many=True).data
            specializations.insert(0, {'code': '', 'name': 'Все'})
            groups = GroupSerializer(Group.objects.all().order_by('course','name'), many=True).data
            courses = list(map(lambda x: {'id': x, 'name': str(x)}, range(1, 5)))
            marks = list(map(lambda x: {'id': x, 'name': str(x)}, range(2, 6)))
            probationers = ProbationerSerializer(Probationer.objects.filter(option__test=test).order_by('-date'), many=True)
            options = OptionSerializer(Option.objects.filter(test=test), many=True).data
            return JsonResponse({
                'testeds': probationers.data,
                'specializations': specializations,
                'groups': groups,
                'courses': courses,
                'options': options,
                'marks': marks
            })
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    else:
        return render_to_response('test_results.html', data)

@login_required
def tested_result(request, id):
    user = request.user
    tested = ProbationerSerializer(get_object_or_404(Probationer, id=id)).data
    tested['answers'] = list(map(lambda answer: answer['answer'], tested['answers']))

    for question in tested['option']['questions']:
        for answer in question['answers']:
            if answer in tested['answers']:
                answer['selected'] = True
            else:
                answer['selected'] = False
    return JsonResponse({'tested': tested})

@login_required
@csrf_exempt
def test_analytic(request, id):
    if request.is_ajax() and request.method == 'POST':
        return HttpResponse('hail')
    else:
        user = request.user
        test = get_object_or_404(Test, id=id,creator=user)
        return render_to_response('analytics_result.html', {'user':user, 'test': test})

def get_page(request, name):
    return render_to_response(name + '.html')