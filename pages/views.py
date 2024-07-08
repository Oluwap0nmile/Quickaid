from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from users.forms import EmergencyContactForm
from users.utils import send_telegram_message
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
        'success': success,    # context variables needed for your existing view
    }
    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')
        if contact_id:
            contact = get_object_or_404(EmergencyContact, id=contact_id, user=request.user)
            contact.delete()
            return redirect('services')
    emergency_contacts = EmergencyContact.objects.filter(user=request.user)

    return render(request, 'services.html', {'emergency_contacts': emergency_contacts})

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

            

            messages.success(request, 'Emergency contact has been registered and notified.')
            return redirect('services')
    else:
        form = EmergencyContactForm()

    return render(request, 'services.html', {'form': form})

@login_required
def send_emergency_message(request):
    if request.method == 'POST':
        contacts = EmergencyContact.objects.filter(user=request.user)
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        message_body = f"Emergency! The user is in danger. Current location: https://www.google.com/maps?q={latitude},{longitude}"
        for contact in contacts:
            send_telegram_message(contact.telegram_chat_id, message_body)  # Ensure 'telegram_chat_id' is the field storing the chat ID
        return redirect('services')
    return render(request, 'services.html')
