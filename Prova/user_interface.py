# -*- coding: utf-8 -*-

'''
Módulo para a interface gráfica
'''

import tkinter
import tkinter.messagebox

from math import ceil

from states import InterfaceState

class UserInterface(tkinter.Frame):

    '''
    Classe para a interface gráfica
    '''

    # Cores
    foreground: str
    background_dark: str
    background_clear: str
    background_normal: str

    store: None # Referência a loja

    # Fontes
    font_title: tuple
    font_buttons: tuple
    font_text: tuple

    # Interfaces
    login_interface: None
    main_interface: None
    insert_interface: None
    edit_interface: None
    product_interface: None

    def __init__(self, store, username, password, master = None):

        self.foreground = "#FFFFFF"
        self.background_dark = "#1A1A1A"
        self.background_clear = "#666666"
        self.background_normal = "#333333"

        super().__init__(master, width = 400, height = 400, bg = self.background_dark)

        self.master = master
        self.store = store

        font_title = ("Arial", 20, "bold")
        font_buttons = ("Arial", 12, "bold")
        font_text = ("Arial", 10)

        self.login_interface = LoginInterface(username,
                                              password,
                                              self.background_dark,
                                              self.background_clear,
                                              self.background_normal,
                                              self.foreground,
                                              font_title,
                                              font_text,
                                              font_buttons,
                                              400,
                                              400,
                                              self)

        self.main_interface = MainInterface(self.background_dark,
                                            self.background_clear,
                                            self.background_normal,
                                            self.foreground,
                                            font_title,
                                            font_text,
                                            font_buttons,
                                            400,
                                            400,
                                            self)

        self.insert_interface = InsertInterface(self.background_dark,
                                                self.background_clear,
                                                self.background_normal,
                                                self.foreground,
                                                font_title,
                                                font_text,
                                                font_buttons,
                                                400,
                                                400,
                                                self)

        self.edit_interface = EditInterface(self.background_dark,
                                            self.background_clear,
                                            self.background_normal,
                                            self.foreground,
                                            font_title,
                                            font_text,
                                            font_buttons,
                                            400,
                                            400,
                                            self)

        self.product_interface = ProductInterface(self.background_dark,
                                                  self.background_clear,
                                                  self.background_normal,
                                                  self.foreground,
                                                  font_title,
                                                  font_text,
                                                  font_buttons,
                                                  400,
                                                  400,
                                                  self)

        self.set_interface(InterfaceState.LOGIN)

    def set_interface(self, state: InterfaceState, product_name: str = None):

        '''
        Define qual interface ficará ativa
        '''

        # Apaga todas as outras interfaces
        self.login_interface.pack_forget()
        self.main_interface.pack_forget()
        self.insert_interface.pack_forget()
        self.edit_interface.pack_forget()
        self.product_interface.pack_forget()
        self.pack_forget()

        # Define a interface alvo com base no estado
        if state == InterfaceState.LOGIN:

            self.login_interface.pack()
        elif state == InterfaceState.MAIN:

            self.main_interface.table_frame.update_table(self.store.get_data()) # Atualiza a tabela

            self.main_interface.pack()
        elif state == InterfaceState.INSERT:

            self.insert_interface.pack()
        elif state == InterfaceState.EDIT:

            self.edit_interface.update_interface(product_name, False) # Atualiza a interface
            self.edit_interface.pack()
        else:

            self.product_interface.update_interface(product_name, True) # Atualiza a interface
            self.product_interface.pack()

        self.pack() # Exibe as interfaces

class Table(tkinter.Frame):

    '''
    Classe usada para a criação de uma planilha com produtos
    '''

    matrix: list # Matriz de widgets
    page_count: int # Quantidade de páginas
    current_page: int # Página atual
    entry_width: int # Largura das entradas
    button_width: int # Largura dos botões
    text_width: int # Largura do texto
    border: int # Tamanho da borda
    bg_n: str # Cor do plano de fundo dos widgets

    # Botões
    next_button: tkinter.Button
    back_button: tkinter.Button

    page_label: tkinter.Label # Enumeração da página
    data: list # Dados

    def __init__(self, bg_d, bg_n, fg, font, width, height, master = None):

        super().__init__(master, width = width, height = height, bg = bg_d)
        self.master = master

        self.bg_n = bg_n

        self.entry_width = 20
        self.button_width = 10
        self.text_width = 10
        self.border = 1

        # Matriz de widgets
        self.matrix = []

        self.name_label = tkinter.Label(self,
                                        bg = bg_d,
                                        fg = fg,
                                        font = font,
                                        height = 2,
                                        width = self.text_width,
                                        bd = 0,
                                        text = "\nNome\n")

        self.amount_label = tkinter.Label(self,
                                          bg = bg_d,
                                          fg = fg,
                                          font = font,
                                          height = 2,
                                          width = self.text_width,
                                          bd = 0,
                                          text = "\nQuantidade\n")

        self.price_label = tkinter.Label(self,
                                         bg = bg_d,
                                         fg = fg,
                                         font = font,
                                         height = 2,
                                         width = self.text_width,
                                         bd = 0,
                                         text = "\nPreço\n")

        self.see_label = tkinter.Label(self,
                                       bg = bg_d,
                                       fg = fg,
                                       font = font,
                                       height = 2,
                                       width = self.text_width,
                                       bd = 0,
                                       text = "\nChecar\n")

        self.edit_label = tkinter.Label(self,
                                        bg = bg_d,
                                        fg = fg,
                                        font = font,
                                        height = 2,
                                        width = self.text_width,
                                        bd = 0,
                                        text = "\nEdição\n")

        self.remove_label = tkinter.Label(self,
                                          bg = bg_d,
                                          fg = fg,
                                          font = font,
                                          height = 2,
                                          width = self.text_width,
                                          bd = 0,
                                          text = "\nRemoção\n")

        self.shopping_cart_label = tkinter.Label(self,
                                                 bg = bg_d,
                                                 fg = fg,
                                                 font = font,
                                                 height = 2,
                                                 width = self.text_width,
                                                 bd = 0,
                                                 text = "\nCarrinho\n")

        # Posiciona os elementos na grade
        self.name_label.grid(row = 0, column = 0, sticky = 'ew')
        self.amount_label.grid(row = 0, column = 1, sticky = 'ew')
        self.price_label.grid(row = 0, column = 2, sticky = 'ew')
        self.see_label.grid(row = 0, column = 3, sticky = 'ew')
        self.edit_label.grid(row = 0, column = 4, sticky = 'ew')
        self.remove_label.grid(row = 0, column = 5, sticky = 'ew')
        self.shopping_cart_label.grid(row = 0, column = 6, sticky = 'ew')

        # Preenche a matriz
        for i in range(10):

            self.matrix.append([])

            for j in range(7):

                if j <= 2: # Entradas

                    self.matrix[i].append(tkinter.Entry(self,
                                                        bg = self.bg_n,
                                                        fg = fg,
                                                        font = font,
                                                        width = self.entry_width,
                                                        bd = self.border,
                                                        state = "disabled",
                                                        disabledbackground = bg_n,
                                                        disabledforeground = fg))
                elif j == 3: # Botão de ver

                    self.matrix[i].append(tkinter.Button(self,
                                                         text = "Ver",
                                                         bg = self.bg_n,
                                                         fg = fg,
                                                         font = font,
                                                         height = 1,
                                                         width = self.button_width,
                                                         bd = 0,
                                                         borderwidth = 0,
                                                         state = "disabled"))
                elif j == 4: # Botão de editar

                    self.matrix[i].append(tkinter.Button(self,
                                                         text = "Editar",
                                                         bg = self.bg_n,
                                                         fg = fg,
                                                         font = font,
                                                         height = 1,
                                                         width = self.button_width,
                                                         bd = 0,
                                                         borderwidth = 0,
                                                         state = "disabled"))
                elif j == 5: # Botão de remover

                    self.matrix[i].append(tkinter.Button(self,
                                                         text = "Remover",
                                                         bg = self.bg_n,
                                                         fg = fg,
                                                         font = font,
                                                         height = 1,
                                                         width = self.button_width,
                                                         bd = 0,
                                                         borderwidth = 0,
                                                         state = "disabled"))
                else: # Botão do carrinho

                    self.matrix[i].append(tkinter.Button(self,
                                                         text = "Adicionar / Remover",
                                                         bg = self.bg_n,
                                                         fg = fg,
                                                         font = font,
                                                         height = 1,
                                                         width = self.button_width,
                                                         bd = 0,
                                                         borderwidth = 0,
                                                         state = "disabled"))

                # Posiciona os elementos na grade
                self.matrix[i][j].grid(row = i + 1, column = j, sticky = 'ew')

        self.page_count = 1
        self.current_page = 0
        self.data = []

        self.next_button = tkinter.Button(self,
                                          text = ">>>",
                                          bg = self.bg_n,
                                          fg = fg,
                                          font = font,
                                          height = 1,
                                          width = 26,
                                          bd = 0,
                                          borderwidth = 0,
                                          command = self.advance_page)

        self.back_button = tkinter.Button(self,
                                          text = "<<<",
                                          bg = self.bg_n,
                                          fg = fg,
                                          font = font,
                                          height = 1,
                                          width = 26,
                                          bd = 0,
                                          borderwidth = 0,
                                          command = self.return_page)

        self.page_label = tkinter.Label(self,
                                        bg = bg_d,
                                        fg = fg,
                                        font = font,
                                        height = 3,
                                        width = 26,
                                        bd = 0)

        # Posiciona os elementos na grade
        self.back_button.grid(row = 11, column = 0)
        self.next_button.grid(row = 11, column = 6)
        self.page_label.grid(row = 11, column = 3)

        self.pack()

    def update_table(self, data: list):

        '''
        Atualiza a planilha
        '''

        # Registra os dados fornecidos
        self.data = data

        # Calcula quantas páginas de 10 linhas são necessárias para exibir os dados
        self.page_count = len(self.data) // 10 + ceil((len(self.data) % 10) / 10)

        # Contagem de página mínima
        if self.page_count < 1:

            self.page_count = 1

        # Define o texto de contagem de páginas
        self.page_label["text"] = str(self.current_page + 1) + ' / ' + str(self.page_count)

        # Gerencia o botão de próximo
        if self.current_page + 1 == self.page_count:

            self.next_button["state"] = "disabled"
        else:

            self.next_button["state"] = "normal"

        # Gerencia o botão de retornar
        if self.current_page == 0:

            self.back_button["state"] = "disabled"
        else:

            self.back_button["state"] = "normal"

        pages = [] # Páginas

        # Define as páginas
        for i in range(self.page_count):

            pages.append([])

            start = i * 10
            end = start + 10

            if end > len(self.data):

                end = len(self.data)

            for j in range(start, end):

                pages[i].append(self.data[j])

        # Insere os dados nas caixas de texto e botões
        for i in range(10):

            for j in range(7):

                self.matrix[i][j]["state"] = "normal" # Habilita a edição nos widgets

                if j <= 2:

                    self.matrix[i][j].delete(0, "end") # Deleta o texto na entrada

                    if len(pages[self.current_page]) - 1 >= i: # Se há um elemento no índice

                        # Preenche os dados na entrada
                        product = pages[self.current_page][i].get_simple_data()
                        self.matrix[i][j].insert(tkinter.INSERT, product[j])

                    self.matrix[i][j]["state"] = "disabled" # Desabilita a edição nos widgets
                else:

                    if len(pages[self.current_page]) - 1 >= i: # Se há um elemento no índice

                        if j == 3: # Botão de ver

                            # Atualiza o produto referenciado pelo botão
                            self.matrix[i][j]["command"] = lambda i = i: \
                            self.see(pages[self.current_page][i].get_simple_data()[0])
                        elif j == 4: # Botão de editar

                            # Atualiza o produto referenciado pelo botão
                            self.matrix[i][j]["command"] = lambda i = i: \
                            self.edit(pages[self.current_page][i].get_simple_data()[0])
                        elif j == 5: # Botão de remover

                            # Atualiza o produto referenciado pelo botão
                            self.matrix[i][j]["command"] = lambda i = i: \
                            self.remove(pages[self.current_page][i].get_simple_data()[0])
                        else: # Botão do carrinho

                            # Atualiza o produto referenciado pelo botão
                            self.matrix[i][j]["command"] = lambda i = i: \
                            self.set_cart_state(pages[self.current_page][i].get_simple_data()[0])

                            # Atualiza a cor do botão com base no carrinho
                            # Caso o produto esteja no carrinho o botão ficará verde
                            if pages[self.current_page][i].get_simple_data()[3]:

                                self.matrix[i][j]["bg"] = "#00A100"
                            else:

                                self.matrix[i][j]["bg"] = self.bg_n
                    else:

                        # Desabilita os botões não usados e redefine a cor deles
                        self.matrix[i][j]["bg"] = self.bg_n
                        self.matrix[i][j]["state"] = "disabled"

    def advance_page(self):

        '''
        Avança uma página
        '''

        if self.current_page + 1 < self.page_count:

            self.current_page += 1

        self.update_table(self.data)

    def return_page(self):

        '''
        Retorna uma página
        '''

        if self.current_page > 0:

            self.current_page -= 1

        self.update_table(self.data)

    def see(self, product_name: str = None):

        '''
        Vai para a página do produto
        '''

        self.master.master.set_interface(InterfaceState.PRODUCT, product_name)

    def edit(self, product_name: str = None):

        '''
        Vai para a página de edição do produto
        '''

        self.master.master.set_interface(InterfaceState.EDIT, product_name)

    def remove(self, product_name: str = None):

        '''
        Remove o produto
        '''

        self.master.master.store.remove_product(product_name)
        self.update_table(self.master.master.store.get_data())

    def set_cart_state(self, product_name: str = None):

        '''
        Adiciona ou remove o produto do carrinho
        '''

        self.master.master.store.set_product_cart_state(product_name)
        self.update_table(self.master.master.store.get_data())

class DataInterface(tkinter.Frame):

    '''
    Descreve uma interface para dados de um produto.
    Esta classe é usada para ser herdada.
    '''

    # Frames
    name_frame: tkinter.Frame
    type_frame: tkinter.Frame
    description_frame: tkinter.Frame
    amount_frame: tkinter.Frame
    price_frame: tkinter.Frame
    cart_state_frame: tkinter.Frame
    button_frame: tkinter.Frame

    # Labels
    title: tkinter.Label
    name_label: tkinter.Label
    type_label: tkinter.Label
    description_label: tkinter.Label
    amount_label: tkinter.Label
    price_label: tkinter.Label
    cart_state_label: tkinter.Label

    # Entradas de texto em geral
    name: tkinter.Entry
    type_: tkinter.Entry
    description: tkinter.Text
    amount: tkinter.Entry
    price: tkinter.Entry
    cart_state: tkinter.Entry

    return_button: tkinter.Button # Botão de retorno

    def __init__(self,
                 bg_d,
                 bg_c,
                 bg_n,
                 fg,
                 font_title,
                 font_text,
                 font_buttons,
                 width,
                 height,
                 master = None):

        super().__init__(master, width = width, height = height, bg = bg_d)
        self.master = master

        self.name_frame = tkinter.Frame(master = self,
                                        width = width,
                                        height = height,
                                        bg = bg_d)

        self.type_frame = tkinter.Frame(master = self,
                                        width = width,
                                        height = height,
                                        bg = bg_d)

        self.description_frame = tkinter.Frame(master = self,
                                               width = width,
                                               height = height,
                                               bg = bg_d)

        self.amount_frame = tkinter.Frame(master = self,
                                          width = width,
                                          height = height,
                                          bg = bg_d)

        self.price_frame = tkinter.Frame(master = self,
                                         width = width,
                                         height = height,
                                         bg = bg_d)

        self.cart_state_frame = tkinter.Frame(master = self,
                                              width = width,
                                              height = height,
                                              bg = bg_d)

        self.button_frame = tkinter.Frame(master = self,
                                          width = width,
                                          height = height,
                                          bg = bg_d)

        self.title = tkinter.Label(self,
                                   bg = bg_d,
                                   fg = fg,
                                   font = font_title,
                                   height = 3,
                                   width = 30,
                                   bd = 0)

        self.name_label = tkinter.Label(self.name_frame,
                                        bg = bg_d,
                                        fg = fg,
                                        font = font_text,
                                        height = 1,
                                        width = 20,
                                        bd = 0,
                                        text = "Nome: ")

        self.type_label = tkinter.Label(self.type_frame,
                                        bg = bg_d,
                                        fg = fg,
                                        font = font_text,
                                        height = 1,
                                        width = 20,
                                        bd = 0,
                                        text = "Tipo: ")

        self.description_label = tkinter.Label(self.description_frame,
                                               bg = bg_d,
                                               fg = fg,
                                               font = font_text,
                                               height = 1,
                                               width = 20,
                                               bd = 0,
                                               text = "Descrição: ")

        self.amount_label = tkinter.Label(self.amount_frame,
                                          bg = bg_d,
                                          fg = fg,
                                          font = font_text,
                                          height = 1,
                                          width = 20,
                                          bd = 0,
                                          text = "Quantidade: ")

        self.price_label = tkinter.Label(self.price_frame,
                                         bg = bg_d,
                                         fg = fg,
                                         font = font_text,
                                         height = 1,
                                         width = 20,
                                         bd = 0,
                                         text = "Preço: ")

        self.cart_state_label = tkinter.Label(self.cart_state_frame,
                                        bg = bg_d,
                                        fg = fg,
                                        font = font_text,
                                        height = 1,
                                        width = 20,
                                        bd = 0,
                                        text = "Está no carrinho: ")

        self.name = tkinter.Entry(self.name_frame,
                                  bg = bg_c,
                                  fg = fg,
                                  font = font_text,
                                  width = 30,
                                  bd = 2,
                                  state = "disabled",
                                  disabledbackground = bg_c,
                                  disabledforeground = fg)

        self.type_ = tkinter.Entry(self.type_frame,
                                   bg = bg_c,
                                   fg = fg,
                                   font = font_text,
                                   width = 30,
                                   bd = 2,
                                   state = "disabled",
                                   disabledbackground = bg_c,
                                   disabledforeground = fg)

        self.description = tkinter.Text(self.description_frame,
                                        bg = bg_c,
                                        fg = fg,
                                        font = font_text,
                                        height = 5,
                                        width = 30,
                                        bd = 0,
                                        borderwidth = 2,
                                        state = "disabled")

        self.amount = tkinter.Entry(self.amount_frame,
                                    bg = bg_c,
                                    fg = fg,
                                    font = font_text,
                                    width = 30,
                                    bd = 2,
                                    state = "disabled",
                                    disabledbackground = bg_c,
                                    disabledforeground = fg)

        self.price = tkinter.Entry(self.price_frame,
                                   bg = bg_c,
                                   fg = fg,
                                   font = font_text,
                                   width = 30,
                                   bd = 2,
                                   state = "disabled",
                                   disabledbackground = bg_c,
                                   disabledforeground = fg)

        self.cart_state = tkinter.Entry(self.cart_state_frame,
                                        bg = bg_c,
                                        fg = fg,
                                        font = font_text,
                                        width = 30,
                                        bd = 2,
                                        state = "disabled",
                                        disabledbackground = bg_c,
                                        disabledforeground = fg)

        self.return_button = tkinter.Button(self.button_frame,
                                            text = "Voltar",
                                            bg = bg_n,
                                            fg = fg,
                                            font = font_buttons,
                                            height = 2,
                                            width = 10,
                                            bd = 0,
                                            borderwidth = 0,
                                            command = self.return_to_main_interface)

        self.button = tkinter.Button(self.button_frame,
                                     bg = bg_n,
                                     fg = fg,
                                     font = font_buttons,
                                     height = 2,
                                     width = 10,
                                     bd = 0,
                                     borderwidth = 0)

        # Posiciona todos os elementos
        self.title.pack(side = "top")
        self.name_label.pack(side = "left", padx = 8)
        self.name.pack(side = "left", padx = 8)
        self.name_frame.pack(padx = 15, pady = 10)
        self.type_label.pack(side = "left", padx = 8)
        self.type_.pack(side = "left", padx = 8)
        self.type_frame.pack(padx = 15, pady = 10)
        self.description_label.pack(side = "left", padx = 8)
        self.description.pack(side = "left", padx = 8)
        self.description_frame.pack(padx = 15, pady = 10)
        self.amount_label.pack(side = "left", padx = 8)
        self.amount.pack(side = "left", padx = 8)
        self.amount_frame.pack(padx = 15, pady = 10)
        self.price_label.pack(side = "left", padx = 8)
        self.price.pack(side = "left", padx = 8)
        self.price_frame.pack(padx = 15, pady = 10)
        self.cart_state_label.pack(side = "left", padx = 8)
        self.cart_state.pack(side = "left", padx = 8)
        self.cart_state_frame.pack(padx = 15, pady = 10)
        self.button.pack(side = "left", padx = 15)
        self.return_button.pack(side = "left", padx = 15)
        self.button_frame.pack(side = "bottom", pady = 30)

    def return_to_main_interface(self):

        '''
        Retorna para o menu.
        '''

        self.master.set_interface(InterfaceState.MAIN)

    def update_interface(self, product_name: list, disable: bool):

        '''
        Atualiza a interface do produto
        '''

        product_data = self.master.store.get_product(product_name) # Obtém os dados do produto
        added_to_card = ''

        # Se o produto está ou não no carrinho
        if product_data[5]:

            added_to_card = "Sim"
        else:

            added_to_card = "Não"

        # Habilita a edição dos widgets
        self.name["state"] = "normal"
        self.type_["state"] = "normal"
        self.description["state"] = "normal"
        self.amount["state"] = "normal"
        self.price["state"] = "normal"
        self.cart_state["state"] = "normal"

        # Apaga os textos nos widgets
        self.name.delete(0, tkinter.END)
        self.type_.delete(0, tkinter.END)
        self.description.delete("1.0", tkinter.END)
        self.amount.delete(0, tkinter.END)
        self.price.delete(0, tkinter.END)
        self.cart_state.delete(0, tkinter.END)

        # Preenche o texto nos widgets
        self.name.insert(tkinter.END, product_data[0])
        self.type_.insert(tkinter.END, product_data[1])
        self.description.insert(tkinter.END, product_data[2])
        self.amount.insert(tkinter.END, product_data[3])
        self.price.insert(tkinter.END, product_data[4])
        self.cart_state.insert(tkinter.END, added_to_card)

        if disable:

            # Desabilita a edição dos widgets
            self.name["state"] = "disabled"
            self.type_["state"] = "disabled"
            self.description["state"] = "disabled"
            self.amount["state"] = "disabled"
            self.price["state"] = "disabled"
            self.cart_state["state"] = "disabled"

    def validate_data(self, inserting: bool, name: str, amount: str, price: str):

        '''
        Valida os dados para a inserção e edição
        '''

        name_is_valid = False # Validade do nome
        values_are_valid = True # Validade dos valores

        if inserting:

            # Verifica se o produto que vai ser inserido já existe, caso exista ele não é válido
            name_is_valid = not self.master.store.has_product(name)
        else:

            # Verifica se o produto que vai ser editado existe
            name_is_valid = self.master.store.has_product(name)

        try:

            # Checa se os valores inserido são reamente números
            amount = int(amount)
            price = float(price)

            # A quantidade não pode ser nula e o preço não pode ser negativo
            if amount <= 0 or price < 0:

                raise ValueError
        except ValueError:

            values_are_valid = False

        # Retorna se o produto é valido ou não
        if name_is_valid and values_are_valid:

            return True
        else:

            return False

class LoginInterface(tkinter.Frame):

    '''
    Descreve uma interface para o login.
    '''

    title: tkinter.Label # Título

    # Frames
    top_frame: tkinter.Frame
    bottom_frame: tkinter.Frame

    # Labels
    username_label: tkinter.Label
    password_label: tkinter.Label

    # Entradas
    username_entry: tkinter.Entry
    password_entry: tkinter.Entry

    enter_button: tkinter.Button # Botão de confirmação

    username: str # Nome de usuário
    password: str # Senha

    def __init__(self,
                 username,
                 password,
                 bg_d,
                 bg_c,
                 bg_n,
                 fg,
                 font_title,
                 font_text,
                 font_buttons,
                 width,
                 height,
                 master = None):

        super().__init__(master, width = width, height = height, bg = bg_d)
        self.master = master
        self.top_frame = tkinter.Frame(master = self, width = width, height = height, bg = bg_d)
        self.bottom_frame = tkinter.Frame(master = self, width = width, height = height, bg = bg_d)

        self.username = username
        self.password = password

        self.title = tkinter.Label(self,
                                   bg = bg_d,
                                   fg = fg,
                                   font = font_title,
                                   height = 3,
                                   width = 30,
                                   bd = 0,
                                   text = "\nLogin\n")

        self.username_label = tkinter.Label(self.top_frame,
                                            bg = bg_d,
                                            fg = fg,
                                            font = font_text,
                                            height = 1,
                                            width = 20,
                                            bd = 0,
                                            text = "Usuário: ")

        self.password_label = tkinter.Label(self.bottom_frame,
                                            bg = bg_d,
                                            fg = fg,
                                            font = font_text,
                                            height = 1,
                                            width = 20,
                                            bd = 0,
                                            text = "Senha: ")

        self.username_entry = tkinter.Entry(self.top_frame,
                                            bg = bg_c,
                                            fg = fg,
                                            font = font_text,
                                            width = 20,
                                            bd = 2)

        self.password_entry = tkinter.Entry(self.bottom_frame,
                                            bg = bg_c,
                                            fg = fg,
                                            font = font_text,
                                            width = 20,
                                            bd = 2,
                                            show = '*')

        self.enter_button = tkinter.Button(self,
                                           text = "Entrar",
                                           bg = bg_n,
                                           fg = fg,
                                           font = font_buttons,
                                           height = 2,
                                           width = 10,
                                           bd = 0,
                                           borderwidth = 0,
                                           command = self.enter)

        # Posiciona todos os widgets
        self.title.pack(side = "top")
        self.username_label.pack(side = "left", padx = 8)
        self.username_entry.pack(side = "left", padx = 8)
        self.password_label.pack(side = "left", padx = 8)
        self.password_entry.pack(side = "left", padx = 8)
        self.top_frame.pack(padx = 10, pady = 10)
        self.bottom_frame.pack(padx = 10, pady = 10)
        self.enter_button.pack(pady = 30)

    def enter(self):

        '''
        Tenta fazer o login
        '''

        # Verifica se o nome de usuário e a senha são iguais
        user_name_matches = self.username_entry.get().rstrip() == self.username
        password_matches = self.password_entry.get().rstrip() == self.password

        if user_name_matches and password_matches:

            self.master.set_interface(InterfaceState.MAIN) # Vai para a tela principal
        else:

            tkinter.messagebox.showerror(title = "Erro",
                                         message = "Nome de usuário ou senha incorretos!")

class MainInterface(tkinter.Frame):

    '''
    Descreve uma interface para a tela principal.
    '''

    # Frames
    top_frame: tkinter.Frame
    table_frame: tkinter.Frame

    product_name_entry: tkinter.Entry # Entrada da pesquisa
    search_button: tkinter.Button # Botão de pesquisa
    insert_button: tkinter.Button # Botão de inserção
    buy_button: tkinter.Button # Botão de compra
    quit_button: tkinter.Button # Botão de saída

    def __init__(self,
                 bg_d,
                 bg_c,
                 bg_n,
                 fg,
                 font_title,
                 font_text,
                 font_buttons,
                 width,
                 height,
                 master = None):

        super().__init__(master, width = width, height = height, bg = bg_d)
        self.master = master
        self.top_frame = tkinter.Frame(master = self, width = width, height = height, bg = bg_d)
        self.table_frame = Table(bg_d, bg_n, fg, font_text, 400, 400, self)

        self.title = tkinter.Label(self,
                                   bg = bg_d,
                                   fg = fg,
                                   font = font_title,
                                   height = 3,
                                   width = 30,
                                   bd = 0,
                                   text = "\nSistema de Supermercado\n")

        self.product_name_entry = tkinter.Entry(self.top_frame,
                                                bg = bg_c,
                                                fg = fg,
                                                font = font_text,
                                                width = 20,
                                                bd = 2)

        self.search_button = tkinter.Button(self.top_frame,
                                            text = "Pesquisar",
                                            bg = bg_n,
                                            fg = fg,
                                            font = font_buttons,
                                            height = 2,
                                            width = 10,
                                            bd = 0,
                                            borderwidth = 0,
                                            command = self.search)

        self.insert_button = tkinter.Button(self.top_frame,
                                            text = "Inserir",
                                            bg = bg_n,
                                            fg = fg,
                                            font = font_buttons,
                                            height = 2,
                                            width = 10,
                                            bd = 0,
                                            borderwidth = 0,
                                            command = self.insert)

        self.buy_button = tkinter.Button(self.top_frame,
                                         text = "Comprar",
                                         bg = "#00A100",
                                         fg = fg,
                                         font = font_buttons,
                                         height = 2,
                                         width = 10,
                                         bd = 0,
                                         borderwidth = 0,
                                         command = self.buy)

        self.quit_button = tkinter.Button(self.top_frame,
                                          text = "Sair",
                                          bg = "#FF0000",
                                          fg = fg,
                                          font = font_buttons,
                                          height = 2,
                                          width = 10,
                                          bd = 0,
                                          borderwidth = 0,
                                          command = self.leave)

        # Posiciona todos os widgets
        self.title.pack(side = "top")
        self.product_name_entry.pack(side = "left", padx = 8)
        self.search_button.pack(side = "left", padx = 8)
        self.insert_button.pack(side = "left", padx = 8)
        self.buy_button.pack(side = "left", padx = 8)
        self.quit_button.pack(side = "left", padx = 8)
        self.top_frame.pack(side = "top", padx = 15, pady = 15)
        self.table_frame.update_table(self.master.store.get_data())
        self.table_frame.pack(side = "bottom", padx = 15, pady = 15)
        self.pack()

    def search(self):

        '''
        Procura por um produto.
        O produto mais próximo ficará no primeiro lugar da tabela.
        '''

        name = self.product_name_entry.get().rstrip() # Obtém o nome

        # Define a tabela para o resultado da pesquisa
        self.table_frame.update_table(self.master.store.search_product(name))

    def insert(self):

        '''
        Vai para a interface de inserção.
        '''

        self.master.set_interface(InterfaceState.INSERT)

    def buy(self):

        '''
        Compra os produtos marcados
        '''

        total_price = self.master.store.buy_products() # Calcula o preço total

        # Mensagem de compra
        tkinter.messagebox.showinfo(title = "Compra",
                                    message = f"Sua compra custou R$ {total_price:.2f}")

        self.table_frame.update_table(self.master.store.get_data())

    def leave(self):

        '''
        Sai do programa
        '''

        self.master.master.destroy()

class InsertInterface(DataInterface):

    '''
    Descreve uma interface para a tela de inserção de dados.
    Esta classe herda da DataInterface. Então conserva vários elementos.
    '''

    def __init__(self,
                 bg_d,
                 bg_c,
                 bg_n,
                 fg,
                 font_title,
                 font_text,
                 font_buttons,
                 width,
                 height,
                 master = None):

        super().__init__(bg_d,
                         bg_c,
                         bg_n,
                         fg,
                         font_title,
                         font_text,
                         font_buttons,
                         width,
                         height,
                         master = master)

        self.master = master
        self.title["text"] = "\nInserir\n" # Redefine o título

        # Habilita a edição de texto
        self.name["state"] = "normal"
        self.type_["state"] = "normal"
        self.description["state"] = "normal"
        self.amount["state"] = "normal"
        self.price["state"] = "normal"

        self.cart_state_frame.pack_forget() # Apaga a exibição do estado do carrinho

        self.button["text"] = "Inserir" # Muda o texto do botão
        self.button["command"] = self.insert # Muda o comando do botão

    def insert(self):

        '''
        Insere o produto no sistema
        '''

        # Obtém os dados sanitizados das entradas de texto
        name = self.name.get().rstrip()
        type_ = self.type_.get().rstrip()
        description = self.description.get("1.0", tkinter.END).rstrip()
        amount = self.amount.get().rstrip()
        price = self.price.get().rstrip()

        # Se os dados são válidos é feita a insersão do produto
        if self.validate_data(True, name, amount, price):

            amount = int(amount)
            price = float(price)

            # Insere o produto
            self.master.store.set_product(name, type_, description, amount, price)

            # Apaga o texto das entradas
            self.name.delete(0, tkinter.END)
            self.type_.delete(0, tkinter.END)
            self.description.delete("1.0", tkinter.END)
            self.amount.delete(0, tkinter.END)
            self.price.delete(0, tkinter.END)
        else:

            tkinter.messagebox.showerror(title = "Erro",
                                         message = "Dados inválidos")

class EditInterface(DataInterface):

    '''
    Descreve uma interface para a tela de edição de dados.
    Esta classe herda da DataInterface. Então conserva vários elementos.
    '''

    def __init__(self,
                 bg_d,
                 bg_c,
                 bg_n,
                 fg,
                 font_title,
                 font_text,
                 font_buttons,
                 width,
                 height,
                 master = None):

        super().__init__(bg_d,
                         bg_c,
                         bg_n,
                         fg,
                         font_title,
                         font_text,
                         font_buttons,
                         width,
                         height,
                         master = master)

        self.master = master
        self.title["text"] = "\nEditar\n" # Redefine o título
        self.button["text"] = "Editar" # Define o texto do botão
        self.button["command"] = self.edit # Define o comando do botão
        self.cart_state_frame.pack_forget() # Apaga a exibição do estado do carrinho

    def edit(self):

        '''
        Edita o produto
        '''

        # Obtém os dados sanitizados das entradas de texto
        name = self.name.get().rstrip()
        type_ = self.type_.get().rstrip()
        description = self.description.get("1.0", tkinter.END).rstrip()
        amount = self.amount.get().rstrip()
        price = self.price.get().rstrip()

        # Se os dados são válidos é feita a edição do produto
        if self.validate_data(False, name, amount, price):

            amount = int(amount)
            price = float(price)

            # Edição do produto
            self.master.store.set_product(name, type_, description, amount, price)
        else:

            tkinter.messagebox.showerror(title = "Erro",
                                         message = "Dados inválidos")

class ProductInterface(DataInterface):

    '''
    Descreve uma interface para a exibição de dados.
    Esta classe herda da DataInterface. Então conserva vários elementos.
    '''

    def __init__(self,
                 bg_d,
                 bg_c,
                 bg_n,
                 fg,
                 font_title,
                 font_text,
                 font_buttons,
                 width,
                 height,
                 master = None):

        super().__init__(bg_d,
                         bg_c,
                         bg_n,
                         fg,
                         font_title,
                         font_text,
                         font_buttons,
                         width,
                         height,
                         master = master)

        self.master = master
        self.title["text"] = "\nProduto\n" # Redefine o título
        self.button.pack_forget() # Apaga o botão
