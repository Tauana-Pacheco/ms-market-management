from werkzeug.security import generate_password_hash, check_password_hash
import random

class UserDomain:
    def __init__(self, nome, cnpj, email, celular, senha=None, senha_hash=None, status="Inativo"):
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.status = status
        self.activation_code = None

        if senha_hash is not None:
            self.senha = senha_hash
        elif senha is not None:
            self.senha = generate_password_hash(senha)
        else:
            raise ValueError("É necessário fornecer uma senha ou senha_hash.")
        
    def verificar_senha(self, senha):
        return(check_password_hash(self.senha, senha))
        
    def ativar_conta(self):
        self.status = "Ativo"

    def gerar_codigo_ativacao(self):
        self.activation_code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return self.activation_code

    def verificar_codigo_ativacao(self, codigo):
        return self.activation_code == codigo
