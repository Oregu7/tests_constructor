from django.shortcuts import render_to_response

# Create your views here.
def index(request):
    return render_to_response('english.html')

def get_page(request, page):
    return render_to_response(page)