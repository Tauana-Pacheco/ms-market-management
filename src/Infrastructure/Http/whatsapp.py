from twilio.rest import Client
from dotenv import load_dotenv
import os 
from Application.Interefaces.message_service_interface import IMessageService

load_dotenv()

class WhatsAppService(IMessageService):
    def __init__(self):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.client = Client(account_sid, auth_token)
        
    def send_message(self, number, message):
        twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        message = self.client.messages.create(
            from_=f'whatsapp:{twilio_phone_number}',
            body=message,
            to=f'whatsapp:{number}'
        )
        return message.sid
