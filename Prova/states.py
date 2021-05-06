# -*- coding: utf-8 -*-

'''
Módulo para a definição dos estados da interface.
'''

from enum import Enum

class InterfaceState(Enum):

    '''
    Enumerador dos estados da interface.
    '''

    LOGIN = 1
    MAIN = 2
    INSERT = 3
    EDIT = 4
    PRODUCT = 5
