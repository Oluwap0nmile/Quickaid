from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.contrib import messages
from .forms import EmergencyContactForm
from users.models import EmergencyContact
from users.utils import send_whatsapp_message

# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')  # Replace 'home' with your homepage URL name
#     else:
#         form = SignUpForm()
#     return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user
            # Redirect to a success page or login view
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


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




