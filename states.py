# -*- coding: utf-8 -*-

'''
Módulo que define os estados
'''

from enum import Enum

class GameState(Enum):

    '''
    Enumerador de estados
    '''

    MENU = 1
    INIT = 2
    SMALL_BLIND = 3
    BIG_BLIND = 4
    PRE_FLOP = 5
    FLOP = 6
    TURN = 7
    RIVER = 8
    COMP = 9
    FINISHED = 10
    EXITING = 11
