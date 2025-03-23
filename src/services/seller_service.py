import random
from app.repository import seller_repository
from app.models.schemas.seller_schema import SellerCreate, SellerActivate
from app.db.session import get_db
from app.core.security import hash_password
from app.services.whatsapp_service import send_whatsapp_code
from fastapi import Depends, HTTPException

def register_seller(seller: SellerCreate, db = Depends(get_db)):
    codigo = str(random.randint(1000, 9999))
    hashed_pwd = hash_password(seller.senha)
    data = seller.dict()
    data["senha"] = hashed_pwd
    data["codigo_ativacao"] = codigo
    seller_obj = seller_repository.create_seller(db, data)
    send_whatsapp_code(seller.celular, codigo)
    return {"message": "Cadastro realizado. Verifique o WhatsApp para ativar."}

def activate_seller(data: SellerActivate, db = Depends(get_db)):
    success = seller_repository.activate_seller_by_code(db, data.celular, data.codigo)
    if not success:
        raise HTTPException(status_code=400, detail="Código inválido ou expirado")
    return {"message": "Conta ativada com sucesso!"}
