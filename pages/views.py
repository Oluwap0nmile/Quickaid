from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from users.forms import EmergencyContactForm
from users.utils import send_whatsapp_message
from users.models import EmergencyContact
# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def services(request):
    success = False
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            emergency_contact = form.save(commit=False)
            emergency_contact.user = request.user
            emergency_contact.save()
            success = True
    else:
        form = EmergencyContactForm()
    
    context = {
        'form': form,
        'success': success,
        # Include any other context variables needed for your existing view
    }
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

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))



# def index(request):
#     return render(request, 'index.html')
# pages/views.py





from django.contrib import messages

@login_required
def emergency_contact_view(request):
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            emergency_contact = form.save(commit=False)
            emergency_contact.user = request.user
            emergency_contact.save()

            # Send WhatsApp message
            to = f"whatsapp:{emergency_contact.contact_phone}"
            body = (
                f"Emergency! {request.user.username} is in an emergency situation. "
                f"Location: https://www.google.com/maps?q={request.POST.get('latitude')},{request.POST.get('longitude')}"
            )
            send_whatsapp_message(to, body)

            messages.success(request, 'Emergency contact has been registered and notified.')
            return redirect('services')
    else:
        form = EmergencyContactForm()

    return render(request, 'services.html', {'form': form})
