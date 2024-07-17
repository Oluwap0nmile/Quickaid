# utils.py
# utils.py
import vonage
from django.conf import settings

def send_sms(to, message):
    client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_API_SECRET)
    sms = vonage.Sms(client)
    
    responseData = sms.send_message({
        "from": "VonageAPI",
        "to": to,
        "text": message,
    })

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
