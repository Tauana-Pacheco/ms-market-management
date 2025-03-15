from flask import Flask
from flask import Blueprint, request, jsonify
from app.core.domain.seller import Seller, db
from flask_jwt_extended import JWTManager, create_access_token
from app.utils.twilio import enviar_codigo_verificacao
from twilio.rest import Client
import os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash

app = Flask(__name__)

load_dotenv()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 

jwt = JWTManager(app)

auth_bp = Blueprint('auth', __name__) # cria um Blueprint "auth" para organizar as rotas do flask e armazena na variável "auth_bp"

@auth_bp.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    seller = Seller.query.filter_by(email=email).first()

    if seller is None or not check_password_hash(seller.senha, senha) is True:
        print(seller)
        print(seller.senha)
        print(senha)
        print(check_password_hash(seller.senha, senha))
        return jsonify({"error": "Credenciais inválidas"}), 401
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200
    


@auth_bp.route('/send_verification_code', methods=['POST']) # rota "/send_verification_code" após Blueprint "auth" para enviar o código de verificação ("http://127.0.0.1:5000/auth/send_verification_code")
def send_verification_code():
    """ rota para enviar um código de verificação via SMS """
    data = request.get_json() # armazena tudo que foi enviado para a rota como "json" na variável "data"
    celular = data.get("celular") # filtra com o ".get()" o celular dentro do objeto json "data"

    seller = Seller.query.filter_by(celular=celular).first() # retorna o celular do seller cadastrado
    if not seller:
        return jsonify({"error": "Número de celular não encontrado"}), 404 # utiliza a biblioteca flask "jsonify" para exibir a mensagem de erro (404-Page Not Found)

    if enviar_codigo_verificacao(celular):
        return jsonify({"message": "Código enviado com sucesso!"}), 200 # utiliza a biblioteca flask "jsonify" para exibir a mensagem desejada (200-Solicitação Bem Sucedida)
    return jsonify({"error": "Erro ao enviar código"}), 500 # utiliza a biblioteca flask "jsonify" para exibir a mensagem de erro (500-Internal Server Error)


@auth_bp.route('/verify_code', methods=['POST']) # rota "/verify_code" após Blueprint "auth" para solicitar a verificação do código ("http://127.0.0.1:5000/auth/verify_code")
def verify_code():
    """ rota para validar o código enviado pelo usuário """
    data = request.get_json()
    celular = data.get("celular")
    codigo = data.get("codigo")

    # Credenciais da Twilio
    account_sid = os.getenv("TWILIO_ACCOUNT_SID") #usa o "os.getenv" do pacote "os" para resgatar as variáveis de ambiente do arquivo ".env" e guardar na variável "account_sid"
    auth_token = os.getenv("TWILIO_AUTH_TOKEN") #usa o "os.getenv" do pacote "os" para resgatar as variáveis de ambiente do arquivo ".env" e guardar na variável "auth_token"
    service_sid = os.getenv("TWILIO_SERVICE_SID") #usa o "os.getenv" do pacote "os" para resgatar as variáveis de ambiente do arquivo ".env" e guardar na variável "service_sid"

    client = Client(account_sid, auth_token) # usa a classe "Client" da biblioteca "twilio.rest" para armazenar o "account_sid" e o "auth_token" na variável "client"

    try: # tratamente de exceção simples
        verification_check = client.verify \
            .v2 \
            .services(service_sid) \
            .verification_checks \
            .create(to=f'+{celular}', code=codigo) # script de verificação base do "Twilio"

        if verification_check.status == "approved": # verifica se o retorno da verificação é "approved"
            seller = Seller.query.filter_by(celular=celular).first() # retorna o celular do seller cadastrado
            if seller:
                seller.status = "Ativo" # em caso do retorno da verificação ser "approved" altera o status do seller para "Ativo"
                db.session.commit() # atualiza o banco de dados
                return jsonify({"message": "Conta ativada com sucesso!"}), 200 # utiliza a biblioteca flask "jsonify" para exibir a mensagem desejada (200-Solicitação Bem Sucedida)
            return jsonify({"error": "Usuário não encontrado"}), 404 # utiliza a biblioteca flask "jsonify" para exibir a mensagem de erro (404-Page Not Found)

        return jsonify({"error": "Código inválido ou expirado"}), 400 # utiliza a biblioteca flask "jsonify" para exibir a mensagem de erro (400-Solicitação Não Encontrada)

    except Exception as e:
        return jsonify({"error": str(e)}), 500 # utiliza a biblioteca flask "jsonify" para exibir a mensagem de erro (500-Internal Server Error)