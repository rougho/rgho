from django.shortcuts import render

# Create your views here.
def index(request):
    name = 'rohi'
    return render(request, 'core/index.html', {'user' : name})