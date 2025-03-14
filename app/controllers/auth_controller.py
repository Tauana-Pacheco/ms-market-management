from flask import Blueprint, request, jsonify
from app.core.domain.seller import Seller, db
from flask_jwt_extended import create_access_token
from app.utils.twilio import enviar_codigo_verificacao
from twilio.rest import Client
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    """ Rota para enviar um código de verificação via SMS """
    data = request.get_json()
    celular = data.get("celular")

    seller = Seller.query.filter_by(celular=celular).first()
    if not seller:
        return jsonify({"error": "Número de celular não encontrado"}), 404

    if enviar_codigo_verificacao(celular):
        return jsonify({"message": "Código enviado com sucesso!"}), 200
    return jsonify({"error": "Erro ao enviar código"}), 500


@auth_bp.route('/verify_code', methods=['POST'])
def verify_code():
    """ Rota para validar o código enviado pelo usuário """
    data = request.get_json()
    celular = data.get("celular")
    codigo = data.get("codigo")

    # Credenciais da Twilio
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    service_sid = os.getenv("TWILIO_SERVICE_SID")

    client = Client(account_sid, auth_token)

    try:
        verification_check = client.verify \
            .v2 \
            .services(service_sid) \
            .verification_checks \
            .create(to=f'+{celular}', code=codigo)

        if verification_check.status == "approved":
            seller = Seller.query.filter_by(celular=celular).first()
            if seller:
                seller.status = "Ativo"
                db.session.commit()
                return jsonify({"message": "Conta ativada com sucesso!"}), 200
            return jsonify({"error": "Usuário não encontrado"}), 404

        return jsonify({"error": "Código inválido ou expirado"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
