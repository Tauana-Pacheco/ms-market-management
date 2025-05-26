from config import db
from datetime import datetime

class Sales(db.Model):
    __tablename__ = 'Vendas'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('Produtos.id'), nullable=False)
    user_email = db.Column(db.String(255), db.ForeignKey('users.email'), nullable=False)
    quantidade_vendida = db.Column(db.Integer, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)

    produto = db.relationship('Products', backref=db.backref('vendas', lazy=True))
    vendedor = db.relationship('User', backref=db.backref('vendas', lazy=True), foreign_keys = [user_email])
    def __init__(self, produto_id, user_email, quantidade_vendida, valor_total, data_venda=None):
        self.produto_id = produto_id
        self.user_email = user_email
        self.quantidade_vendida = quantidade_vendida
        self.valor_total = valor_total
        self.data_venda = data_venda or datetime.utcnow()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def from_domain(cls, domain):
        return cls(
            produto_id=domain.produto_id,
            user_email=domain.user_email,
            quantidade_vendida=domain.quantidade_vendida,
            data_venda=domain.data_venda,
            valor_total=domain.valor_total
    )