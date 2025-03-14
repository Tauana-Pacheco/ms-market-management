from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10), default="inativo")
    codigo_verificação = db.Column(db.String(4), nullable=True)

    def __init__(self, nome, cnpj, email, celular, senha):
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.senha = senha