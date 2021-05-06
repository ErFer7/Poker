# -*- coding: utf-8 -*-

'''
Sistema de vendas de um supermercado.
Este sistema tem elementos de uma loja online também.
Autor: Eric Fernandes Evaristo

Python: 3.9.2
'''

import tkinter as tk

from user_interface import UserInterface
from store_system import StoreSystem

USERNAME = "user"
PASSWORD = "123456"

root = tk.Tk("Supermercado - Sistema de vendas")

store = StoreSystem() # Instância do sistema de loja
user_interface = UserInterface(store, USERNAME, PASSWORD, master = root) # Instância da interface

user_interface.master.title("Supermercado - Sistema de vendas")

user_interface.mainloop() # Executa o loop princicpal
