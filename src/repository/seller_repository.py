from sqlalchemy.orm import Session
from app.models.seller_model import Seller

def create_seller(db: Session, seller_data: dict):
    seller = Seller(**seller_data)
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller

def get_seller_by_celular(db: Session, celular: str):
    return db.query(Seller).filter(Seller.celular == celular).first()

def activate_seller_by_code(db: Session, celular: str, codigo: str):
    seller = get_seller_by_celular(db, celular)
    if seller and seller.codigo_ativacao == codigo:
        seller.status = True
        seller.codigo_ativacao = None
        db.commit()
        return True
    return False