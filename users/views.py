from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
# from django.contrib import messages
from .forms import EmergencyContactForm
from users.models import EmergencyContact
import vonage

from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.conf import settings
import json
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import send_sms
from .models import EmergencyContact

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
            # to = f"whatsapp:{emergency_contact.contact_phone}"
            # body = (
            #     f"Emergency!  is in an emergency situation. "
            #     f"Location: https://www.google.com/maps?q={request.POST.get('latitude')},{request.POST.get('longitude')}"
            # )
            # send_whatsapp_message(to, body)

            # messages.success(request, 'Emergency contact has been registered and notified.')
            return redirect('services')
    else:
        form = EmergencyContactForm()

    return render(request, 'services.html', {'form': form})

class EmergencyContactDeleteView(DeleteView):
    model = EmergencyContact
    template_name = 'users/emergency_contact_confirm_delete.html'
    success_url = reverse_lazy('emergency_contact')

@login_required
def send_emergency_sms(request):
    user = request.user
    # Assuming user's location is stored in the first emergency contact for simplicity
    emergency_contact = EmergencyContact.objects.filter(user=user).first()
    
    if emergency_contact:
        location_url = f"https://www.google.com/maps?q={emergency_contact.latitude},{emergency_contact.longitude}"
        message = f"Emergency! {user.get_full_name()} is in an emergency. Location: {location_url}"
        
        # Initialize Vonage client
        client = vonage.Client(key='55aace73', secret='fqAQgXcNxNpa2uyj')
        sms = vonage.Sms(client)

        contacts = EmergencyContact.objects.filter(user=user)
        for contact in contacts:
            responseData = sms.send_message({
                "from": "VonageAPI",
                "to": contact.contact_phone,
                "text": message,
            })

            if responseData["messages"][0]["status"] == "0":
                print(f"Message sent to {contact.contact_name}")
            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

        return render(request, 'services.html', {'message': 'Emergency messages sent successfully!'})
    else:
        return render(request, 'services.html', {'message': 'No emergency contact found!'})

@csrf_exempt
@login_required
def update_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        user.latitude = data.get('latitude')
        user.longitude = data.get('longitude')
        user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)


