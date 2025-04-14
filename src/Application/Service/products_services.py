from Infrastructure.Models.products_model import Products
from Domain.products_domain import ProductDomain

class ProductService:

    @staticmethod
    def create_product(data):

        product_domain = ProductDomain(

            nome = data['nome'],
            preco = data['preco'],
            quantidade = data['quantidade'],
            imagem = data['imagem'],
            status=data.get('status', 'Inativo')
        )

        product = Products.from_domain(product_domain)
        product.save()
        

        return {'message': 'Produto Adicionado'}