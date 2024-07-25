from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, EmergencyContactForm
from users.models import EmergencyContact
import requests
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.conf import settings
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess

# Login view
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

# Register view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# def scan_wifi():
#     result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'], capture_output=True, text=True).stdout
#     access_points = []
#     lines = result.split('\n')
#     for i in range(len(lines)):
#         if 'BSSID' in lines[i]:
#             mac_address = lines[i].split(':')[1].strip()
#             signal_strength = int(lines[i + 1].split(':')[1].strip().replace('%', ''))
#             access_points.append({'macAddress': mac_address, 'signalStrength': signal_strength})
#     return access_points

# Emergency contact view
@login_required
def emergency_contact_view(request):
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            emergency_contact = form.save(commit=False)
            emergency_contact.user = request.user
            emergency_contact.save()

            message = f"Hello {emergency_contact.contact_name}, please start a chat with our bot to confirm your chat ID."
            send_telegram_message(emergency_contact.contact_phone, message)
            return redirect('services')
    else:
        form = EmergencyContactForm()
    return render(request, 'services.html', {'form': form})

# Delete emergency contact view
class EmergencyContactDeleteView(DeleteView):
    model = EmergencyContact
    template_name = 'users/emergency_contact_confirm_delete.html'
    success_url = reverse_lazy('emergency_contact')

# Telegram bot token
bot_token = settings.TELEGRAM_BOT_TOKEN
YOUR_API_KEY = settings.GOOGLE_API_KEY

# Function to send Telegram message
def send_telegram_message(chat_id, message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

# Send emergency SMS view
@login_required



def send_emergency_sms(request):
    user = request.user
    emergency_contacts = EmergencyContact.objects.filter(user=user)

    if not emergency_contacts.exists():
        return HttpResponse("No emergency contacts found.", status=404)

    user_profile = emergency_contacts.first()
    latitude = DEFAULT_LATITUDE
    longitude = DEFAULT_LONGITUDE

    if latitude is None or longitude is None:
        latitude, longitude = get_location()
        if latitude is None or longitude is None:
            return HttpResponse("Could not retrieve location.", status=500)

    location_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    message = f"Emergency! {user.username} is in an emergency and needs your help. Location: {location_url}"

    for contact in emergency_contacts:
        if contact.chat_id:
            response = send_telegram_message(contact.chat_id, message)
            print(response)

    return HttpResponse("Emergency messages sent successfully.")

DEFAULT_LATITUDE = 7.759997711285218   # Example: New York City Latitude
DEFAULT_LONGITUDE = 4.601843448762301 # Example: New York City Longitude
# Save location
@login_required
@csrf_exempt


def save_location(request):
    if request.method == 'POST':
        # Always use default location coordinates
        latitude = DEFAULT_LATITUDE
        longitude = DEFAULT_LONGITUDE
        
        # Get the user's emergency contact profile
        user_profile = EmergencyContact.objects.get(user=request.user)
        user_profile.latitude = latitude
        user_profile.longitude = longitude
        user_profile.save()
        
        return JsonResponse({'status': 'success', 'latitude': latitude, 'longitude': longitude})
    
    return JsonResponse({'status': 'error'})

def get_location_from_access_points(access_points):
    import requests

    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=YOUR_API_KEY'
    data = {
        'wifiAccessPoints': access_points
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        location = response.json().get('location')
        return location
    return None

# Register chat ID view
@login_required
def register_chat_id(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        contact_id = request.POST.get('contact_id')
        contact = EmergencyContact.objects.get(id=contact_id, user=request.user)
        contact.chat_id = chat_id
        contact.save()
        return redirect('services')
    return JsonResponse({'status': 'error'})

# Telegram bot handler functions
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

def start(update, context):
    update.message.reply_text('Hello! Send /getid to get your chat ID.')

def get_id(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text(f'Your chat ID is: {chat_id}')

def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getid", get_id))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()




def get_location():
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={settings.GOOGLE_API_KEY}'
    response = requests.post(url)
    if response.status_code == 200:
        location = response.json()
        latitude = location.get('location', {}).get('lat', None)
        longitude = location.get('location', {}).get('lng', None)
        return latitude, longitude
    else:
        return None, None