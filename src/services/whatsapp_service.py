from app.core.config import settings
# Simulando envio via Twilio

def send_whatsapp_code(celular: str, codigo: str):
    print(f"[Simulado] Enviando WhatsApp para {celular} com o código: {codigo}")