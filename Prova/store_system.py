# -*- coding: utf-8 -*-

'''
Módulo para o sistema de supermercado e produtos
'''

from difflib import SequenceMatcher

from file_system import FileSystem

class StoreSystem():

    '''
    Sistema de produtos
    '''

    products: dict # Dicionário para armazenar os produtos
    file_system: FileSystem  # Sistema de arquivos

    def __init__(self):

        self.products = {}
        self.file_system = FileSystem("ProductData.json")

        data = self.file_system.get_data() # Obtém os dados o sistema de arquivos

        # Instancia os produtos
        for element in data:

            self.products[element[0]] = Product(element[0],
                                                element[1],
                                                element[2],
                                                element[3],
                                                element[4],
                                                element[5])

    def has_product(self, name: str):

        '''
        Verifica se o produto já existe no sistema
        '''

        if name in self.products.keys():

            return True
        else:

            return False

    def set_product(self, name: str, type_: str, description: str, amount: int, price: float):

        '''
        Insere ou edita um produto
        '''

        if not self.has_product(name): # Instancia um produto caso ele não exista

            self.products[name] = Product(name,
                                          type_,
                                          description,
                                          amount,
                                          price,
                                          False)
        else: # Edita o produto caso ele exista

            self.products[name].edit(type_, description, amount, price)

        # Salva a alteração na memória do sistema de arquivos
        self.file_system.set_element(name, self.products[name].get_data())

    def get_product(self, name: str):

        '''
        Retorna os dados de um produto
        '''

        return [name] + self.products[name].get_data()

    def set_product_cart_state(self, name: str):

        '''
        Adiciona o produto no carrinho de compras
        '''

        self.products[name].set_cart_state()
        self.file_system.set_element(name, self.products[name].get_data())

    def buy_products(self):

        '''
        Processa os produtos para a compra e retorna o custo
        '''

        total_price = 0.0 # Preço total

        keys = list(self.products.keys()) # Nome dos produtos

        for k in keys:

            product_data = self.products[k].get_data() # Obtém os dados de um produto

            if product_data[4]: # Caso o produto esteja no carrinho de compras

                total_price += self.products[k].buy() # Compra o produto e armazena o custo

                # Define as alterações do produto
                self.set_product(k,
                                 product_data[0],
                                 product_data[1],
                                 product_data[2] - 1,
                                 product_data[3])

                # Remove o produto caso a quantidade dele chegue a zero
                if product_data[2] - 1 == 0:

                    self.remove_product(k)

        return total_price

    def remove_product(self, name: str):

        '''
        Remove um produto
        '''

        del self.products[name]
        self.file_system.remove_element(name)

    def get_data(self):

        '''
        Retorna uma lista de produtos
        '''

        return self.build_list_from_dict(self.products.keys())

    def search_product(self, name: str):

        '''
        Retorna uma matriz de produtos sorteada por proximidade com o nome
        '''

        keys = self.products.keys() # Nome dos produtos

        # Sorteia lista de chaves por similaridade
        keys = sorted(keys,
                      key = lambda key: self.string_simmilarity(key, name),
                      reverse = True)

        return self.build_list_from_dict(keys)

    def string_simmilarity(self, string_a, string_b):

        '''
        Retorna o nível de similaridade de dois strings
        '''

        return SequenceMatcher(None, string_a, string_b).ratio()

    def build_list_from_dict(self, keys: list):

        '''
        Constrói uma lista a partir de um dicionário e lista de chaves
        '''

        product_list = []

        for k in keys:

            product_list.append(self.products[k])

        return product_list

class Product():

    '''
    Descreve um produto no sistema.
    '''

    name: str # Nome
    type_: str # Tipo
    description: str # Descrição
    amount: int # Quantidade
    price: float # Preço
    added_to_cart: bool # Adicionado no carrinho ou não

    def __init__(self,
                 name: str,
                 type_: str,
                 description: str,
                 amount: int,
                 price: float,
                 added_to_cart: bool):

        self.name = name
        self.type_ = type_
        self.description = description
        self.amount = amount
        self.price = price
        self.added_to_cart = added_to_cart

    def edit(self, type_: str, description: str, amount: int, price: float):

        '''
        Edita o produto.
        O nome do produto não deve ser passado na lista de parâmetros.
        '''

        self.type_ = type_
        self.description = description
        self.amount = amount
        self.price = price

    def get_simple_data(self):

        '''
        Retorna os dados simplificados.
        '''

        return [self.name, str(self.amount), f"R$ {self.price:.2f}", self.added_to_cart]

    def get_data(self):

        '''
        Retorna os dados.
        '''

        return [self.type_, self.description, self.amount, self.price, self.added_to_cart]

    def set_cart_state(self):

        '''
        Adiciona o produto no carrinho.
        '''

        if self.added_to_cart:

            self.added_to_cart = False
        else:

            self.added_to_cart = True

    def buy(self):

        '''
        Processa a compra deste produto
        '''

        self.amount -= 1
        return self.price
