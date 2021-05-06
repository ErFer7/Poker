# -*- coding: utf-8 -*-

'''
Módulo para a interface gráfica
'''

from math import ceil

import tkinter
import tkinter.messagebox
import file_system

class Application(tkinter.Frame):

    '''
    Aplicação com interface gráfica
    '''

    # Declarações com anotações
    title: tkinter.Label
    insert_screen_button: tkinter.Button
    remove_screen_button: tkinter.Button
    edit_screen_button: tkinter.Button
    show_screen_button: tkinter.Button
    search_screen_button: tkinter.Button
    quit_button: tkinter.Button
    version: tkinter.Label
    return_button: tkinter.Button
    name: tkinter.Label
    address: tkinter.Label
    phone: tkinter.Label
    email: tkinter.Label
    name_input: tkinter.Entry
    address_input: tkinter.Entry
    phone_input: tkinter.Entry
    email_input: tkinter.Entry
    insert_button: tkinter.Button
    remove_button: tkinter.Button
    verify_button: tkinter.Button
    edit_button: tkinter.Button
    search_button: tkinter.Button
    label_frame: tkinter.Frame
    entry_frame: tkinter.Frame
    button_frame: tkinter.Frame
    table_frame: None
    phone_list: file_system.PhoneList
    background_dark: str
    background_normal: str
    background_clear: str
    foreground: str

    def __init__(self, master = None):

        # Cores
        self.background_dark = "#1A1A1A"
        self.background_normal = "#333333"
        self.background_clear = "#666666"
        self.foreground = "#FFFFFF"

        super().__init__(master, width = 400, height = 400, bg = self.background_dark)

        self.master = master

        # Inicializa os frames
        self.label_frame = tkinter.Frame(self,
                                         width = 400,
                                         height = 100,
                                         bg = self.background_dark)
        self.entry_frame = tkinter.Frame(self,
                                         width = 400,
                                         height = 100,
                                         bg = self.background_dark)
        self.button_frame = tkinter.Frame(self,
                                          width = 400,
                                          height = 100,
                                          bg = self.background_dark)
        self.table_frame = Table(self,
                                 width = 400,
                                 height = 100,
                                 bg = self.background_dark)

        # Inicializa a lista telefônica
        self.phone_list = file_system.PhoneList()

        self.pack()
        self.create_widgets()

    def create_widgets(self):

        '''
        Cria os widgets e preenche a janela do app
        '''

        # Fontes
        font_title = ("Arial", 20, "bold")
        font_buttons = ("Arial", 12, "bold")
        font_text = ("Arial", 10)

        self.title = tkinter.Label(self,
                                   bg = self.background_dark,
                                   fg = self.foreground,
                                   font = font_title,
                                   height = 3,
                                   width = 30,
                                   bd = 0,
                                   text = "\nLista Telefônica\n")

        self.name = tkinter.Label(self.label_frame,
                                  bg = self.background_dark,
                                  fg = self.foreground,
                                  font = font_text,
                                  height = 3,
                                  width = 20,
                                  bd = 0,
                                  text = "\nNome\n")

        self.address = tkinter.Label(self.label_frame,
                                     bg = self.background_dark,
                                     fg = self.foreground,
                                     font = font_text,
                                     height = 3,
                                     width = 20,
                                     bd = 0,
                                     text = "\nEndereço\n")

        self.phone = tkinter.Label(self.label_frame,
                                   bg = self.background_dark,
                                   fg = self.foreground,
                                   font = font_text,
                                   height = 3,
                                   width = 20,
                                   bd = 0,
                                   text = "\nNúmero\n")

        self.email = tkinter.Label(self.label_frame,
                                   bg = self.background_dark,
                                   fg = self.foreground,
                                   font = font_text,
                                   height = 3,
                                   width = 20,
                                   bd = 0,
                                   text = "\nEmail\n")

        self.name_input = tkinter.Entry(self.entry_frame,
                                        bg = self.background_clear,
                                        fg = self.foreground,
                                        font = font_text,
                                        width = 20,
                                        bd = 2)

        self.address_input = tkinter.Entry(self.entry_frame,
                                           bg = self.background_clear,
                                           fg = self.foreground,
                                           font = font_text,
                                           width = 20,
                                           bd = 2)

        self.phone_input = tkinter.Entry(self.entry_frame,
                                         bg = self.background_clear,
                                         fg = self.foreground,
                                         font = font_text,
                                         width = 20,
                                         bd = 2)

        self.email_input = tkinter.Entry(self.entry_frame,
                                         bg = self.background_clear,
                                         fg = self.foreground,
                                         font = font_text,
                                         width = 20,
                                         bd = 2)

        self.insert_button = tkinter.Button(self.button_frame,
                                            text = "Inserir",
                                            bg = self.background_normal,
                                            fg = self.foreground,
                                            font = font_buttons,
                                            height = 2,
                                            width = 10,
                                            bd = 0,
                                            borderwidth = 0,
                                            command = self.insert)

        self.remove_button = tkinter.Button(self.button_frame,
                                            text = "Remover",
                                            bg = self.background_normal,
                                            fg = self.foreground,
                                            font = font_buttons,
                                            height = 2,
                                            width = 10,
                                            bd = 0,
                                            borderwidth = 0,
                                            command = self.remove)

        self.edit_button = tkinter.Button(self.button_frame,
                                          text = "Editar",
                                          bg = self.background_normal,
                                          fg = self.foreground,
                                          font = font_buttons,
                                          height = 2,
                                          width = 10,
                                          bd = 0,
                                          borderwidth = 0,
                                          command = self.edit)

        self.search_button = tkinter.Button(self.button_frame,
                                            text = "Pesquisar",
                                            bg = self.background_normal,
                                            fg = self.foreground,
                                            font = font_buttons,
                                            height = 2,
                                            width = 10,
                                            bd = 0,
                                            borderwidth = 0,
                                            command = self.search)

        self.quit_button = tkinter.Button(self.button_frame,
                                          text = "Sair",
                                          bg = "#FF0000",
                                          fg = self.foreground,
                                          font = font_buttons,
                                          height = 2,
                                          width = 10,
                                          bd = 0,
                                          borderwidth = 0,
                                          command = self.leave)

        # Posiciona todos os widgets
        self.title.pack(side = "top")
        self.name.pack(side = "left")
        self.address.pack(side = "left")
        self.phone.pack(side = "left")
        self.email.pack(side = "left")
        self.label_frame.pack(side = "top", padx = 10)

        self.name_input.pack(side = "left", padx = 8)
        self.address_input.pack(side = "left", padx = 8)
        self.phone_input.pack(side = "left", padx = 8)
        self.email_input.pack(side = "left", padx = 8)
        self.entry_frame.pack(side = "top", padx = 10)

        self.insert_button.pack(side = "left", padx = 10)
        self.remove_button.pack(side = "left", padx = 10)
        self.edit_button.pack(side = "left", padx = 10)
        self.search_button.pack(side = "left", padx = 10)
        self.quit_button.pack(side = "left", padx = 10)
        self.button_frame.pack(side = "top", padx = 10, pady = 15)

        self.table_frame.update_table(self.phone_list.get_data())
        self.table_frame.pack(side = "bottom", padx = 15, pady = 15)

    def insert(self):

        '''
        Insere os dados no arquivo
        '''

        name = self.name_input.get().rstrip()

        # Caso o nome não esteja na lista
        if not self.phone_list.has_name(name):

            # Obtém os dados
            address = self.address_input.get().rstrip()
            phone = self.phone_input.get().rstrip()
            email = self.email_input.get().rstrip()

            # Insere o nome e dados na lista
            self.phone_list.set_data(name, address, phone, email)

            # Apaga o texto do campo de texto
            self.name_input.delete(0, "end")
            self.address_input.delete(0, "end")
            self.phone_input.delete(0, "end")
            self.email_input.delete(0, "end")

            # Atualiza a tabela
            self.table_frame.update_table(self.phone_list.get_data())
        else:

            tkinter.messagebox.showerror(title = "Erro",
                                         message = "O nome já existe na lista!")

    def remove(self):

        '''
        Remove os dados no arquivo
        '''

        name = self.name_input.get().rstrip()

        # Caso o nome esteja na lista
        if self.phone_list.has_name(name):

            self.phone_list.remove(name) # Remove os dados e o nome

            # Apaga o texto do campo de texto
            self.name_input.delete(0, "end")
            self.address_input.delete(0, "end")
            self.phone_input.delete(0, "end")
            self.email_input.delete(0, "end")

            # Atualiza a tabela
            self.table_frame.update_table(self.phone_list.get_data())
        else:

            tkinter.messagebox.showerror(title = "Erro",
                                         message = "O nome não está na lista!")

    def edit(self):

        '''
        Edita os dados
        '''

        name = self.name_input.get().rstrip()

        # Caso o nome esteja na lista
        if self.phone_list.has_name(name):

            # Obtém os daddos
            address = self.address_input.get().rstrip()
            phone = self.phone_input.get().rstrip()
            email = self.email_input.get().rstrip()

            # Redefine dados já existentes
            self.phone_list.set_data(name, address, phone, email)

            # Apaga o texto do campo de texto
            self.name_input.delete(0, "end")
            self.address_input.delete(0, "end")
            self.phone_input.delete(0, "end")
            self.email_input.delete(0, "end")

            # Atualiza a tabela
            self.table_frame.update_table(self.phone_list.get_data())
        else:

            tkinter.messagebox.showerror(title = "Erro",
                                         message = "O nome não está na lista!")

    def search(self):

        '''
        Procura os dados
        '''

        name = self.name_input.get().rstrip()

        # Caso o nome esteja na lista
        if self.phone_list.has_name(name):

            # Apaga o texto do campo de texto
            self.address_input.delete(0, "end")
            self.phone_input.delete(0, "end")
            self.email_input.delete(0, "end")

            # Insere os dados no campo de texto
            self.address_input.insert(tkinter.INSERT, self.phone_list.get_user_data(name)[0])
            self.phone_input.insert(tkinter.INSERT, self.phone_list.get_user_data(name)[1])
            self.email_input.insert(tkinter.INSERT, self.phone_list.get_user_data(name)[2])
        else:

            tkinter.messagebox.showwarning(title = "Aviso",
                                           message = "O nome não está na lista." \
                                                     "Cheque a lista para ver os resultados")

        # Redefine a tabela para exibir os resultados de acordo com o nome
        self.table_frame.update_table(self.phone_list.search_data(name))

    def leave(self):

        '''
        Sai do programa
        '''

        self.phone_list.write_file()
        self.master.destroy()


class Table(tkinter.Frame):

    '''
    Classe usada para a criação de uma planilha
    '''

    # Declarações com anotações
    matrix: list
    page_count: int
    current_page: int
    font: tuple
    width: int
    border: int
    background_normal: str
    foreground: str
    next_button: tkinter.Button
    back_button: tkinter.Button
    page_label: tkinter.Label
    data: list

    def __init__(self, master = None, width = None, height = None, bg = None):

        super().__init__(master, width = width, height = height, bg = bg)

        # Cores
        self.background_normal = "#333333"
        self.foreground = "#FFFFFF"

        self.master = master
        self.font = ("Arial", 10)
        self.width = 30
        self.border = 1

        # Matriz de widgets de entrada para a tabela
        self.matrix = []

        # Preenche a matriz
        for i in range(10):

            self.matrix.append([])

            for j in range(4):

                self.matrix[i].append(tkinter.Entry(self,
                                                    bg = self.background_normal,
                                                    fg = self.foreground,
                                                    font = self.font,
                                                    width = self.width,
                                                    bd = self.border,
                                                    state = "disabled",
                                                    disabledbackground = self.background_normal,
                                                    disabledforeground = self.foreground))

                self.matrix[i][j].grid(row = i, column = j)

        self.page_count = 1
        self.current_page = 0
        self.data = []

        self.next_button = tkinter.Button(self,
                                          text = ">>>",
                                          bg = self.background_normal,
                                          fg = self.foreground,
                                          font = self.font,
                                          height = 1,
                                          width = 26,
                                          bd = 0,
                                          borderwidth = 0,
                                          command = self.advance_page)

        self.back_button = tkinter.Button(self,
                                          text = "<<<",
                                          bg = self.background_normal,
                                          fg = self.foreground,
                                          font = self.font,
                                          height = 1,
                                          width = 26,
                                          bd = 0,
                                          borderwidth = 0,
                                          command = self.return_page)

        self.page_label = tkinter.Label(self,
                                        bg = bg,
                                        fg = self.foreground,
                                        font = self.font,
                                        height = 3,
                                        width = 26,
                                        bd = 0)

        self.back_button.grid(row = 10, column = 0)
        self.next_button.grid(row = 10, column = 3)
        self.page_label.grid(row = 10, column = 1)

        self.pack()

    def update_table(self, data: list):

        '''
        Atualiza a planilha
        '''

        # Registra os dados fornecidos
        self.data = data

        # Calcula quantas páginas de 10 linhas são necessárias para exibir os dados
        self.page_count = len(self.data) // 10 + ceil((len(self.data) % 10) / 10)

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

        # Contagem de página mínima
        if self.page_count < 1:

            self.page_count = 1

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

        # Insere os dados nas caixas de texto
        for i in range(10):

            for j in range(4):

                self.matrix[i][j]["state"] = "normal"
                self.matrix[i][j].delete(0, "end")

                if len(pages[self.current_page]) - 1 >= i:

                    self.matrix[i][j].insert(tkinter.INSERT, pages[self.current_page][i][j])

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
