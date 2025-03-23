from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas.seller_schema import SellerCreate, SellerActivate
from app.services.seller_service import register_seller, activate_seller

router = APIRouter()

@router.post("/register")
def register(seller: SellerCreate):
    return register_seller(seller)

@router.post("/activate")
def activate(data: SellerActivate):
    return activate_seller(data)