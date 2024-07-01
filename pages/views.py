from django.shortcuts import render,redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def department(request):
    return render(request, 'department.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')


# def index(request):
#     return render(request, 'index.html')