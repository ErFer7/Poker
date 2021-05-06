# -*- coding: utf-8 -*-

'''
Módulo para o sistema de arquivos
'''

import os
import json

from difflib import SequenceMatcher

class PhoneList():

    '''
    Classe que descreve o comportamento da lista telefônica
    '''

    phone_list: dict

    def __init__(self):

        # Armazena todos os dados em um dicionário
        self.phone_list = {}

        # Caso o arquivo exista ele é lido
        if os.path.exists("Phone list.json"):

            with open("Phone list.json", 'r') as phone_list:

                phone_list_json = phone_list.read()

            self.phone_list = json.loads(phone_list_json)

    def write_file(self):

        '''
        Salva os dados
        '''

        with open("Phone list.json", 'w') as phone_list:

            phone_list_json = json.dumps(self.phone_list, indent = 4)
            phone_list.write(phone_list_json)

    def set_data(self, name: str, address: str, phone: str, email: str):

        '''
        Insere os dados de uma pessoa
        '''

        self.phone_list[name] = (address, phone, email)
        self.write_file()

    def remove(self, name):

        '''
        Remove os dados de uma pessoa
        '''

        del self.phone_list[name]
        self.write_file()

    def get_data(self):

        '''
        Retorna uma matriz de dados
        '''

        matrix = []

        for k in self.phone_list.keys():

            matrix.append([k, self.phone_list[k][0], self.phone_list[k][1], self.phone_list[k][2]])

        return matrix

    def get_user_data(self, name: str) -> tuple:

        '''
        Procura por um nome
        '''

        if name in self.phone_list.keys():

            return self.phone_list[name]
        else:

            return None

    def has_name(self, name):

        '''
        Verifica se a lista tem o nome
        '''

        if name in self.phone_list.keys():

            return True
        else:

            return False

    def search_data(self, name):

        '''
        Retorna uma matriz de dados sorteada por proximidade com o nome
        '''

        keys = self.phone_list.keys()

        # Sorteia lista de chaves por similaridade
        keys = sorted(keys, key = lambda key: self.string_simmilarity(key, name), reverse = True)

        matrix = []

        for k in keys:

            matrix.append([k, self.phone_list[k][0], self.phone_list[k][1], self.phone_list[k][2]])

        return matrix

    def string_simmilarity(self, string_a, string_b):

        '''
        Retorna o nível de similaridade de dois strings
        '''

        return SequenceMatcher(None, string_a, string_b).ratio()
