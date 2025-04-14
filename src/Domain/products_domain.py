class ProductDomain:
    def __init__(self, nome, preco, quantidade, imagem, status="Inativo"):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.imagem = imagem
        self.status = status
    
        