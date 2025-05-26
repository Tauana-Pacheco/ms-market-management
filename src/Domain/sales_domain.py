from datetime import datetime
from typing import Optional

class SalesDomain:
    def __init__(self, produto_id:int, user_email:str, quantidade_vendida:int, valor_total:float, data_venda:Optional[datetime]=None):
        self.produto_id = produto_id
        self.user_email = user_email
        self.quantidade_vendida = quantidade_vendida
        self.data_venda = data_venda
        self.valor_total = valor_total