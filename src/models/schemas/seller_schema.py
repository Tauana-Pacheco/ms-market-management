from pydantic import BaseModel, EmailStr

class SellerCreate(BaseModel):
    nome: str
    cnpj: str
    email: EmailStr
    celular: str
    senha: str

class SellerActivate(BaseModel):
    celular: str
    codigo: str