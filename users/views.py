from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from testsConstructor.helpers import check_sign_in, models_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from constructor.models import Test, Option, Query
from constructor.serializers import OptionSecondSerializer, OptionSerializer, QuerySerializer
from tests.models import Probationer
from tests.serializers import ProbationerSerializer
from .models import Group, Specialization
from .serializers import GroupSerializer, SpecializationSerializer
from django.contrib.auth.decorators import login_required
from rest_framework import status
from xlsxwriter.workbook import Workbook
from django.utils import formats
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

def inc_answer(answer, tes_answers):
    for tes_answer in tes_answers:
        if answer['id'] == tes_answer['id']:
            answer['analytics'] += 1

@login_required
@csrf_exempt
def print_results(request, id):
    if request.method == "POST":
        data = request.POST
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        testeds_sheet = workbook.add_worksheet("Тестируемые")
        questions_sheet = workbook.add_worksheet("Статистика")
        #Оформление
        title = workbook.add_format(Format.title)
        sub_title = workbook.add_format(Format.sub_title)
        thead = workbook.add_format(Format.thead)
        item = workbook.add_format(Format.item)
        formula = workbook.add_format(Format.formula_res)
        formula2 = workbook.add_format(Format.formula_res2)
        merge_format = workbook.add_format(Format.merge_format)
        #Получаем индексы тестируемых
        testeds_index = data.get('testeds','')
        if testeds_index:
            testeds_index = testeds_index.split(",")
            testeds = Probationer.objects.filter(id__in=testeds_index)
        else:
            testeds = []
        #Поучаем тест
        test = get_object_or_404(Test, id=id)

        #Заполнеяем данными
        for index in range(1,7):
            testeds_sheet.set_column(index, index,  20)

        testeds_sheet.merge_range("B2:G2", "Тест на тему : "+test.title, title)
        testeds_sheet.merge_range("B3:G3", "Предмет : "+test.category.name, sub_title)
        testeds_sheet.merge_range("B4:G4", "Разработал(а) : "+test.creator.get_full_name(), sub_title)

        questions_sheet.merge_range("B2:G2", "Тест на тему : "+test.title, title)
        questions_sheet.merge_range("B3:G3", "Предмет : "+test.category.name, sub_title)
        questions_sheet.merge_range("B4:G4", "Разработал(а) : "+test.creator.get_full_name(), sub_title)

        #Параметры поиска
        testeds_sheet.merge_range("B7:G7", "Параметры Поиска", title)
        questions_sheet.merge_range("B7:G7", "Параметры Поиска", title)
        search_ind = 8
        for key in data.keys():
            if key == "option":
                if len(data[key]):
                    option = Option.objects.get(id=data[key])
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Вариант', option.number, search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Вариант', option.number, search_ind)
                else:
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Вариант', "-", search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Вариант', "-", search_ind)
            elif key == "spec":
                if len(data[key]):
                    spec = Specialization.objects.get(code=data[key])
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Специализация', spec.name, search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Специализация', spec.name, search_ind)
                else:
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Специализация', "-", search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Специализация', "-", search_ind)
            elif key == "group":
                if len(data[key]):
                    group = Group.objects.get(id=data[key])
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Группа', group.name, search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Группа', group.name, search_ind)
                else:
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Группа', "-", search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Группа', "-", search_ind)
            elif key == "course":
                if len(data[key]):
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Курс', data[key], search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Курс', data[key], search_ind)
                else:
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Курс', "-", search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Курс', "-", search_ind)
            elif key == "mark":
                if len(data[key]):
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Отметка', data[key], search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Отметка', data[key], search_ind)
                else:
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Отметка', "-", search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Отметка', "-", search_ind)
            elif key == "dateF":
                if len(data[key]):
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Дата От', data[key], search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Дата От', data[key], search_ind)
                else:
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Дата От', "-", search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Дата От', "-", search_ind)
            elif key == "dateL":
                if len(data[key]):
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Дата До', data[key], search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Дата До', data[key], search_ind)
                else:
                    Format().write_param(testeds_sheet, sub_title, formula2, 'Дата До', "-", search_ind)
                    Format().write_param(questions_sheet, sub_title, formula2, 'Дата До', "-", search_ind)
            else:
                continue

            search_ind += 1

        #Тестируемые
        testeds_sheet.merge_range("B17:G17", "Результаты", title)
        titles = ['Вариант', 'Группа', 'Тестируемый', 'Отметка', 'Процент', 'Дата']
        Format().write_thead(testeds_sheet, thead, titles, 17, 1)
        tested_inrex = 18
        for tested in testeds:
            testeds_sheet.write(tested_inrex, 1, tested.option.number, item)
            testeds_sheet.write(tested_inrex, 2, tested.user.study_group.name, item)
            testeds_sheet.write(tested_inrex, 3, tested.user.get_full_name(), item)
            testeds_sheet.write(tested_inrex, 4, tested.mark, item)
            testeds_sheet.write(tested_inrex, 5, tested.precent, item)
            testeds_sheet.write(tested_inrex, 6, formats.date_format(tested.date, 'd-m-Y'), item)
            tested_inrex += 1

        testeds_sheet.write_formula('E%d' % (tested_inrex + 1), '{=AVERAGE(E18:E%d)}' % tested_inrex, formula)
        testeds_sheet.write_formula('F%d' % (tested_inrex + 1), '{=AVERAGE(F18:F%d)}' % tested_inrex, formula)

        #Заполняем 2 лист
        questions_sheet.merge_range("B17:G17", "Статистика", title)
        questions_sheet.set_column("H:H",  40)
        questions_sheet.set_column("I:I",  20)
        questions_sheet.set_column("J:J",  30)
        questions_sheet.set_column("B:G",  15)

        questions = QuerySerializer(Query.objects.filter(test=test), many=True).data
        testeds = ProbationerSerializer(testeds, many=True).data
        for tested in testeds:
            tested['answers'] = list(map(lambda answer: answer['answer'], tested['answers']))

        for question in questions:
            for answer in question['answers']:
                for tested in testeds:
                    inc_answer(answer, tested['answers'])


        question_index = 19
        questions_sheet.merge_range("B18:G18", "Вопросы", thead)
        questions_sheet.write("H18", "Ответы", thead)
        questions_sheet.write("I18", "Правильность", thead)
        questions_sheet.write("J18", "Количество Ответивших", thead)

        for question in questions:
            answers_len = len(question['answers'])
            questions_sheet.merge_range("B%d:G%d" % (question_index, question_index - 1 + answers_len), question['text'], merge_format)
            for answer in question['answers']:
                questions_sheet.write("H%d" % question_index, answer['text'], item)
                questions_sheet.write("I%d" % question_index, answer['correct'], item)
                questions_sheet.write("J%d" % question_index, answer['analytics'], item)
                question_index += 1



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