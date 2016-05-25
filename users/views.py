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
from xlsxwriter.workbook import Workbook
from .excel import Format
import io
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
                'marks': marks,
                'test': id
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

@login_required
@csrf_exempt
def print_results(request, id):
    if request.method == "POST":
        data = request.POST
        print(data)
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        testeds_sheet = workbook.add_worksheet("Тестируемые")

        #Оформление шапки
        title = workbook.add_format(Format.title)
        sub_title = workbook.add_format(Format.sub_title)
        #Получаем индексы тестируемых
        testeds_index = data.get('testeds').split(",")
        testeds = ProbationerSerializer(Probationer.objects.filter(id__in=testeds_index), many=True).data
        #Поучаем тест
        test = get_object_or_404(Test, id=id)

        #Заполнеяем данными
        testeds_sheet.merge_range("B2:G2", "Тест на тему : "+test.title, title)
        testeds_sheet.merge_range("B3:G3", "Предмет : "+test.category.name, sub_title)
        testeds_sheet.merge_range("B4:G4", "Разработал(а) : "+test.creator.get_full_name(), sub_title)
        for index in range(len(testeds)):
            tested = testeds[index]
            testeds_sheet.write(index + 5, 0, tested['user']['last_name'])

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=testeds.xlsx"
        return response
    else:
        return Http404(status=status.HTTP_400_BAD_REQUEST)

@login_required
def get_page(request, name):
    return render_to_response(name + '.html')