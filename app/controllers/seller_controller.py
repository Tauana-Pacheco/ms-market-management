from flask import Blueprint, request, jsonify
from app.core.domain.seller import Seller, db
from app.utils.twilio import enviar_codigo_verificacao

seller_bp = Blueprint('seller', __name__)

@seller_bp.route('/register', methods=['POST'])
def register_seller():
    data = request.get_json()

    nome = data['nome']
    cnpj = data['cnpj']
    email = data['email']
    celular = data['celular']
    senha = data['senha']


    seller = Seller(nome=nome, cnpj=cnpj, email=email, celular=celular, senha=senha)
    db.session.add(seller)
    db.session.commit()

    codigo = enviar_codigo_verificacao(celular)

    seller.codigo_verificação = codigo

    db.session.commit()

    return jsonify({"message": "cadastro realizado com sucesso, código de verificação enviado."}), 201