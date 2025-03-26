from flask import json
from Infrastructure.Models.user_model import User
from Infrastructure.Http.whatsapp import WhatsAppService, send_whatsapp_message
from Domain.user_domain import UserDomain
from flask_jwt_extended import create_access_token
from datetime import timedelta


class UserService: 
  def __init__(self):
        self.whatsapp_service = WhatsAppService()

  # user_domainlorem = UserDomain("Mini Mercado Exemplo", "12345678000199", "exemplo@mercadinho.com", "5511985327304", "senha123")
    

  @staticmethod
  def register_user(data):
      if not all(key in data for key in ['nome', 'cnpj', 'email', 'celular', 'senha']):
        return {'error': 'Dados incompletos, verique!'}

      user = User(
              nome=data['nome'],
              cnpj=data['cnpj'],
              email=data['email'],
              celular=data['celular'],
              senha=data['senha'],
              status='Inativo'
          )
      
      lorem = UserDomain(
            nome=data['nome'],
            cnpj=data['cnpj'],
            email=data['email'],
            celular=data['celular'],
            senha=data['senha'],
            status='Inativo'
     )


      activation_code = lorem.gerar_codigo_ativacao()
      user.activation_code = activation_code
      user.save()

      message = f'Seu código de ativação é: {activation_code}'
      send_whatsapp_message(user.celular, message)

      return {'message': 'Usuário registrado com sucesso! Aguarde a ativação.'}

 
  @staticmethod
  def activate_user(data):
    if 'email' not in data or 'codigo' not in data:
        return {'error': 'Dados incompletos, verifique!'}

    user = User.find_by_email(data['email'])
    if user:
        print(f"Esperado: {user.activation_code}, Recebido: {str(data['codigo'])}")
        user_domain = UserDomain(
            nome=user.nome,
            cnpj=user.cnpj,
            email=user.email,
            celular=user.celular,
            senha=user.senha,
            status=user.status
        )
        user_domain.activation_code = user.activation_code

        if user_domain.verificar_codigo_ativacao(data['codigo']):
            user_domain.ativar_conta()
            user.status = user_domain.status
            #user.activation_code = None  # Remove o código após a ativação
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
            senha=user.senha,
            status=user.status
        )

        if user_domain.verificar_senha(data['senha']):
            if user.status == 'Ativo':
                access_token = create_access_token(
                    identity=json.dumps({'email': user.email, 'cnpj': user.cnpj}),
                    expires_delta=timedelta(hours=1)
                )
                return {'access_token': access_token}
            return {'error': 'Conta inativa. Por favor, ative sua conta.'}
    return {'error': 'Credenciais inválidas.'}