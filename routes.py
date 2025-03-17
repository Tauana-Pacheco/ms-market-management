from flask import Flask, request, jsonify
from twilio.rest import Client
import os
import dotenv
from flask import Blueprint, request, jsonify
from app.core.domain.seller import Seller, db
from app.utils.twilio import enviar_codigo_verificacao
from werkzeug.security import generate_password_hash

app = Flask(__name__)

dotenv.load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

seller_bp = Blueprint('seller', __name__)

#Jullyen vai testar essa parte, e deixar funcionando de acordo com o número no .env
@seller_bp.route('/register', methods=['POST'])
def register_seller():
    data = request.get_json()

    nome = data['nome']
    cnpj = data['cnpj']
    email = data['email']
    celular = data['celular']
    senha = generate_password_hash(data['senha'])

    # criar e salvar o seller no banco
    seller = Seller(nome=nome, cnpj=cnpj, email=email, celular=celular, senha=senha)
    db.session.add(seller)
    db.session.commit()

    # enviar código de verificação via Twilio
    sucesso = enviar_codigo_verificacao(celular)

    if not sucesso:
        return jsonify({"error": "Falha ao enviar código de verificação"}), 500

    return jsonify({"message": "Cadastro realizado com sucesso. Código de verificação enviado!"}), 201



@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()
    to_number = data.get("to")
    message_body = data.get("message")

    if not to_number or not message_body:
        return jsonify({"error": "Número e mensagem são obrigatórios"}), 400

    try:
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:{to_number}",
            body=message_body
        )
        return jsonify({"message": "Mensagem enviada!", "sid": message.sid})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
