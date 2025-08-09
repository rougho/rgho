from django.shortcuts import render

def handle_404(request, exception):
    return render(request, 'errors/404.html', status=404)