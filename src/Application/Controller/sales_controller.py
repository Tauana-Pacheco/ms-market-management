from Infrastructure.Models.sales_model import Sales
from Infrastructure.Helpers.jwt_helper import token_obrigatorio
from flask import request, jsonify
from datetime import datetime
from Infrastructure.Models.products_model import Products
from Domain.sales_domain import SalesDomain

class SalesController:
    
    @staticmethod
    @token_obrigatorio
    def registrar_venda(user_email):
        data = request.get_json()

        try:
            sales_domain = SalesDomain(
                produto_id=data['produto_id'],
                user_email=user_email,
                quantidade_vendida=int(data["quantidade_vendida"]),
                valor_total=float(data['valor_total']),
            )
        except (KeyError, ValueError) as e:
            return jsonify({"error":"Dados Inválidos ou incompletos"}), 400
        
        produto = Products.query.get(sales_domain.produto_id)
        if not produto:
            return jsonify({"error": "Produto não encontrado"}), 404
        
        if produto.user_email != user_email:
            return jsonify({"error": "Você não tem permissão para vender este produto"}), 403
        
        if produto.quantidade < sales_domain.quantidade_vendida:
            return jsonify({"error": "Estoque insuficiente"}), 400
        
        produto.quantidade -= sales_domain.quantidade_vendida
        produto.save()

        venda = Sales.from_domain(sales_domain)
        venda.save()

        return jsonify({"message": "Venda realizada com sucesso!"}), 201
    
    @staticmethod
    @token_obrigatorio
    def historico_vendas(user_email):
        vendas = Sales.query.filter(user_email==user_email).all()

        return jsonify(
                        [
                        {"id": venda.id,
                        "produto_id": venda.produto_id,
                        "quantidade_vendida": venda.quantidade_vendida,
                        "data_venda": venda.data_venda.strftime('%Y-%m-%d %H:%M:%S'),
                        "valor_total": float(venda.valor_total)
                        }
                        for venda in vendas
                    ]
                )