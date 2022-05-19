# -*- coding: utf: 8 -*-

'''
Módulo que define a interface do usuário
'''

import os

class UserInterface():

    '''
    Classe que define o comportamento da interface
    '''

    def __init__(self):
        pass

    def build_menu_interface(self):

        '''
        Constrói a interface do menu
        '''

        self.clear_console()

        print(" _______             __                              \n" + \
              "|       \\           |  \\                           \n" + \
              "| $$$$$$$\\  ______  | $$   __   ______    ______    \n" + \
              "| $$__/ $$ /      \\ | $$  /  \\ /      \\  /      \\\n" + \
              "| $$    $$|  $$$$$$\\| $$_/  $$|  $$$$$$\\|  $$$$$$\\\n" + \
              "| $$$$$$$ | $$  | $$| $$   $$ | $$    $$| $$   \\$$  \n" + \
              "| $$      | $$__/ $$| $$$$$$\\ | $$$$$$$$| $$        \n" + \
              "| $$       \\$$    $$| $$  \\$$\\ \\$$     \\| $$    \n" + \
              " \\$$        \\$$$$$$  \\$$   \\$$  \\$$$$$$$ \\$$   \n")

        print("___________________________________________________________________________________")

    def build_game_interface(self, players: list, communitary_cards: list, player_count: int, pot: int, main_player_index: int, current_player_index: int, message: str):

        '''
        Constrói a interface do jogo
        '''

        self.clear_console()

        print("___________________________________________________________________________________")
        print(message)
        print("___________________________________________________________________________________")

        for i in range(player_count):

            if i != current_player_index:

                print(players[i].get_name())
            else:

                print(f"{players[i].get_name()} <<<")

        print("___________________________________________________________________________________")
        print(f"Pote: {pot} --- Suas fichas: {players[main_player_index].get_chips()}")
        print(f"Suas cartas: {players[main_player_index].get_card_list()}")
        print(f"Cartas comunitária: {communitary_cards}")
        print("___________________________________________________________________________________")

    def build_turnover_interface(self, players: list, communitary_cards: list, player_count: int, pot: int):

        '''
        Constrói a interface do fim de uma rodada
        '''

        self.clear_console()
        print("___________________________________________________________________________________")
        print("Fim da rodada")
        print("___________________________________________________________________________________")

        for i in range(player_count):

            print(f"{i + 1}º {players[i].get_name()} - Cartas: {players[i].get_card_list()} - Nível: {players[i].get_hand_level():.2f}")

        print("___________________________________________________________________________________")
        print(f"Cartas comunitárias: {communitary_cards}")
        print("___________________________________________________________________________________")

        print(f"{players[0].get_name()} ganhou a rodada e levou {pot} fichas!")
        print("___________________________________________________________________________________")

    def build_gameover_interface(self, players: list):

        '''
        Constrói a interface do fim do jogo
        '''

        self.clear_console()
        print("___________________________________________________________________________________")
        print("Fim de jogo")
        print("___________________________________________________________________________________")
        print(f"{players[0].get_name()} Ganhou o jogo!")
        print("___________________________________________________________________________________")

    def clear_console(self):

        '''
        Limpa a tela
        '''

        os.system("cls" if os.name == "nt" else "clear")
