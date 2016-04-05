from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from constructor.models import Query, Answer
import json

def index(request):
    return render_to_response('analytics.html')

def get_page(request, page):
    return render_to_response(page)

@csrf_exempt
def save_analytics(request):
    data = json.loads(request.POST['data'])
    print(data)
    for analytic in data:
        if analytic['current_answer']:
            answer = Answer.objects.get(id=analytic['current_answer'], query__id=analytic['id'])
            answer.analytics += 1
            answer.save()

    return JsonResponse({'success': True})