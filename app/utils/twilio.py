from twilio.rest import Client
import os
from app.core.domain.seller import Seller, db

def enviar_codigo_verificacao(celular):
    """ Envia um código de verificação para o celular do usuário via Twilio Verify """
    
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    service_sid = os.getenv("TWILIO_SERVICE_SID")

    client = Client(account_sid, auth_token)
    
    seller = Seller.query.filter_by(celular=celular).first()
    if not seller:
        return False  # Retorna erro se o celular não existir no sistema
    
    try:
        verification = client.verify \
            .v2 \
            .services(service_sid) \
            .verifications \
            .create(to=f'+{celular}', channel='sms')  # Pode usar 'whatsapp' se preferir
        
        print("Código de verificação enviado:", verification.status)  # Log para debug
        return True  # Retorna sucesso
    
    except Exception as e:
        print("Erro ao enviar código:", str(e))  # Log de erro
        return False

