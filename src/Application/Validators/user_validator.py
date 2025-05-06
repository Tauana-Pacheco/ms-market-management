def validar_dados_usuario(data):
    campos_obrigatorios = ['nome', 'email', 'cnpj', 'celular', 'senha']
    if not all(key in data for key in campos_obrigatorios):
        return 'Dados incompletos, verifique'
    return None