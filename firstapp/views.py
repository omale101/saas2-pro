from django.shortcuts import render

def home(request):
    return render(request, 'firstapp/index.html')