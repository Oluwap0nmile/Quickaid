from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def services(request):
    return render(request, 'services.html')

@login_required(login_url='login')
def department(request):
    return render(request, 'department.html')

def login(request):
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')


# def index(request):
#     return render(request, 'index.html')