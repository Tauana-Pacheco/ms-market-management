from Infrastructure.Models.user_model import User
from Domain.user_domain import UserDomain
from Application.Interefaces.message_service_interface import IMessageService
from Infrastructure.Helpers.jwt_helper import gerar_token
from Application.Validators.user_validator import validar_dados_usuario

class UserService:
    def __init__(self, message_service: IMessageService):
        self.message_service = message_service

    def register_user(self, data):
        erro = validar_dados_usuario(data)
        if erro:
            return{'error': erro}

       
        user_domain = UserDomain(
            nome=data['nome'],
            cnpj=data['cnpj'],
            email=data['email'],
            celular=data['celular'],
            senha=data['senha'],
            status='Inativo'
        )

       
        activation_code = user_domain.gerar_codigo_ativacao()

        user = User(
            nome=user_domain.nome,
            cnpj=user_domain.cnpj,
            email=user_domain.email,
            celular=user_domain.celular,
            senha=user_domain.senha,
            status=user_domain.status,
            activation_code=activation_code  
        )
        user.save()

        message = f'Seu código de ativação é: {activation_code}'
        self.message_service.send_message(user.celular, message)

        return {'message': 'Usuário registrado com sucesso! Aguarde a ativação.'}
    
    
    def activate_user(self, data):
        user = User.find_by_email(data['email'])
        if user:
            user_domain = UserDomain(
                nome=user.nome,
                cnpj=user.cnpj,
                email=user.email,
                celular=user.celular,
                senha=user.senha,
                status=user.status
            )
            user_domain.activation_code = user.activation_code

            if user_domain.verificar_codigo_ativacao(data['code']):
                user_domain.ativar_conta()
                user.status = user_domain.status
                user.activation_code = None
                user.save()
                return {'message': 'Conta ativada com sucesso.'}

        return {'error': 'Código de ativação inválido.'}
    
    def login_user(self, data):
            user = User.find_by_email(data['email'])
            if user:
             user_domain = UserDomain(
                    nome=user.nome,
                    cnpj=user.cnpj,
                    email=user.email,
                    celular=user.celular,
                    senha_hash=user.senha,
                    status=user.status
             )
            if user_domain.verificar_senha(data['senha']):
                if user.status == 'Ativo':
                    token = gerar_token(user.email)
                    return {'message': 'Login bem-sucedido.', 'token': token}
                return {'error': 'Conta inativa. Por favor, ative sua conta.'}
            return {'error': 'Credenciais inválidas.'}