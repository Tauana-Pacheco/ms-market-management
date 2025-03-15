from flask import Blueprint, request, jsonify
from app.core.domain.seller import Seller, db
from app.utils.twilio import enviar_codigo_verificacao
from werkzeug.security import generate_password_hash

seller_bp = Blueprint('seller', __name__)

@seller_bp.route('/register', methods=['POST'])
def register_seller():
    data = request.get_json()

    nome = data['nome']
    cnpj = data['cnpj']
    email = data['email']
    celular = data['celular']
    senha = generate_password_hash(data['senha'])

    # Criar e salvar o seller no banco
    seller = Seller(nome=nome, cnpj=cnpj, email=email, celular=celular, senha=senha)
    db.session.add(seller)
    db.session.commit()

    # Enviar código de verificação via Twilio
    sucesso = enviar_codigo_verificacao(celular)

    if not sucesso:
        return jsonify({"error": "Falha ao enviar código de verificação"}), 500

    return jsonify({"message": "Cadastro realizado com sucesso. Código de verificação enviado!"}), 201