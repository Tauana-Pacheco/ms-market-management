from flask_sqlalchemy import SQLAlchemy
from config import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    activation_code = db.Column(db.String(4), nullable=True)
    status = db.Column(db.String(10), default="inativo")

    @classmethod
    def from_domain(cls, user_domain):
        return cls(
            nome=user_domain.nome,
            cnpj=user_domain.cnpj,
            email=user_domain.email,
            celular=user_domain.celular,
            senha=user_domain.senha,
            status=user_domain.status
        )

    def save(self):
      db.session.add(self)
      db.session.commit()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()
