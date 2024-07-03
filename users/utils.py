# users/utils.py

from twilio.rest import Client

def send_whatsapp_message(to, body):
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_='whatsapp:+12056864631',  # This is Twilio's sandbox number
        to=to
    )
    return message.sid