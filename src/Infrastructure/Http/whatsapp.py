from twilio.rest import Client
from dotenv import load_dotenv
import os 

load_dotenv()

class WhatsAppService:
    def __init__(self):
        self.client = Client('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN')
        
def send_whatsapp_message(to, message):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=f'whatsapp:{twilio_phone_number}',
        body=message,
        to=f'whatsapp:{to}'
    )
    return message.sid