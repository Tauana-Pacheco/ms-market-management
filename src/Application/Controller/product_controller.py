from flask import request, jsonify, abort
from Infrastructure.Models.products_model import Products
import os
from flask import send_from_directory
from Infrastructure.Helpers.jwt_helper import token_obrigatorio

class ProductController:
    @staticmethod
    @token_obrigatorio
    def register_product(user_email):
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')
        status = request.form.get('status', 'Inativo')
        imagem = request.files.get('imagem')

        if not nome or not preco or not quantidade:
            return jsonify({'error': 'Nome, preço e quantidade são obrigatórios'}), 400

        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'src', 'assets')
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        imagem_path = None
        if imagem:
            imagem_path_abs = os.path.join(UPLOAD_FOLDER, imagem.filename)
            imagem.save(imagem_path_abs)
            imagem_path = f'/assets/{imagem.filename}'

        novo_produto = Products(
            nome=nome,
            preco=preco,
            quantidade=quantidade,
            status=status,
            imagem=imagem_path,
            user_email=user_email  # ← associar o dono
        )

        novo_produto.save()
        return jsonify({'message': 'Produto registrado com sucesso!'}), 201


    @staticmethod
    def listar_produtos():
        produtos = Products.query.all()
        return jsonify([{
            "id": p.id,
            "nome": p.nome,
            "preco": float(p.preco),
            "quantidade": p.quantidade,
            "status": p.status,
            "imagem": p.imagem
        } for p in produtos])
    
    @staticmethod
    def serve_assets(filename):
        assets_dir = os.path.join(os.getcwd(), 'src', 'assets')
        return send_from_directory(assets_dir, filename)

    @staticmethod
    def atualizar_imagem(produto_id):
        imagem = request.files.get('imagem')
        if not imagem:
            return jsonify({'error': 'Nenhuma imagem enviada'}), 400

        produto = Products.query.get(produto_id)
        if not produto:
            return jsonify({'error': 'Produto não encontrado'}), 404

        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'src', 'assets')
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        imagem_path = os.path.join(UPLOAD_FOLDER, imagem.filename)
        imagem.save(imagem_path)
        produto.imagem = f'/assets/{imagem.filename}'
        produto.save()

        return jsonify({'message': 'Imagem atualizada com sucesso'}), 200
    
    @staticmethod
    def get_produto(id):
        produto = Products.query.get(id)
        if not produto:
            abort(404, description="Produto não encontrado")

        return jsonify({
            "id": produto.id,
            "nome": produto.nome,
            "preco": float(produto.preco),
            "quantidade": produto.quantidade,
            "status": produto.status,
            "imagem": produto.imagem,
        })

    @staticmethod
    @token_obrigatorio
    def atualizar_produto(user_email, id):
        data = request.get_json()
        produto = Products.query.get(id)

        if not produto:
            return jsonify({'error': 'Produto não encontrado'}), 404

        if produto.user_email != user_email:
            return jsonify({'error': 'Você não tem permissão para editar este produto'}), 403

        produto.nome = data.get('nome', produto.nome)
        produto.preco = data.get('preco', produto.preco)
        produto.quantidade = data.get('quantidade', produto.quantidade)
        produto.status = data.get('status', produto.status)

        produto.save()
        return jsonify({'message': 'Produto atualizado com sucesso'}), 200
