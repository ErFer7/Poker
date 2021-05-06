# -*- coding: utf-8 -*-

'''
Lista telefônica, atividade AA3

Feito por Eric Fernandes Evaristo

Python: 3.9.2
'''

import tkinter as tk
import application

root = tk.Tk("Lista telefônica")

app = application.Application(master = root)

app.master.title("Lista telefônica")

app.mainloop()
