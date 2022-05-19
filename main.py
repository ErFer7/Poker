# -*- coding: utf-8 -*-

'''
Jogo de poker feito por Eric Fernandes Evaristo

v1.1.3

Tipo de poker: Texas Hold’Em (Porém com modificações para deixar o jogo mais simples).

Python 3.9.2
'''

from states import GameState
from poker import Poker

state = GameState.MENU
exit_states = [GameState.COMP, GameState.FINISHED, GameState.EXITING]

while state != GameState.EXITING:

    poker_game = Poker(2, 500)

    while poker_game.get_state() == GameState.INIT:

        while poker_game.get_state() not in exit_states:

            poker_game.hand_behaviour()

            if poker_game.get_state() != GameState.COMP:

                poker_game.player_behaviour()

        poker_game.restore_game()

    state = poker_game.get_state()
