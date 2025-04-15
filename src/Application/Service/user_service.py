from Infrastructure.Models.user_model import User
from Domain.user_domain import UserDomain
from Infrastructure.Http.whatsapp import WhatsAppService
from Infrastructure.Helpers.jwt_helper import gerar_token
class UserService:
    def __init__(self):
        self.whatsapp_service = WhatsAppService()

    @staticmethod
    def register_user(data):
        if not all(key in data for key in ['nome', 'cnpj', 'email', 'celular', 'senha']):
            return {'error': 'Dados incompletos, verifique!'}

        # Cria a instância do UserDomain
        user_domain = UserDomain(
            nome=data['nome'],
            cnpj=data['cnpj'],
            email=data['email'],
            celular=data['celular'],
            senha=data['senha'],
            status='Inativo'
        )

        # Aqui é onde o código de ativação é gerado
        activation_code = user_domain.gerar_codigo_ativacao()

        # Cria o usuário no banco de dados
        user = User(
            nome=user_domain.nome,
            cnpj=user_domain.cnpj,
            email=user_domain.email,
            celular=user_domain.celular,
            senha=user_domain.senha,
            status=user_domain.status,
            activation_code=activation_code  # Define o código gerado
        )
        user.save()

        # Envia a mensagem de ativação via WhatsApp
        message = f'Seu código de ativação é: {activation_code}'
        UserService().whatsapp_service.send_message(user.celular, message)

        return {'message': 'Usuário registrado com sucesso! Aguarde a ativação.'}
    
    
    @staticmethod
    def activate_user(data):  
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
                user.activation_code = None  # Remove o código após a ativação
                user.save()
                return {'message': 'Conta ativada com sucesso.'}
        return {'error': 'Código de ativação inválido.'}
  
    @staticmethod
    def login_user(data):
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