from flask_sqlalchemy import SQLAlchemy
from config import db

class Products(db.Model):
    __tablename__ = 'Produtos'

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(255), nullable = False)
    preco = db.Column(db.Numeric(10, 2), nullable = False)
    quantidade = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String(10), default = 'Inativo')
    imagem = db.Column(db.String(255))
    user_email = db.Column(db.String(120), nullable=False)

    @classmethod
    def from_domain(cls, product_domain):
        return cls(
            nome = product_domain.nome,
            preco = product_domain.preco,
            quantidade = product_domain.quantidade,
            status = product_domain.status,
            imagem = product_domain.imagem
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

