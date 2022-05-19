# -*- coding: utf-8 -*-

'''
Módulo que contém a classe que descreve o comportamento do jogo.
'''

from time import time_ns
from random import randint, seed

from UI import UserInterface
from players import Player, Bot
from cards import CardDeck
from states import GameState

class Poker():

    '''
    Classe que gerencia o próprio jogo
    '''

    _pot: int
    _min_bet: int
    _current_bet: int
    _current_player_index: int
    _main_player_index: int
    _message: str
    _players_list: list
    _communitary_cards: list
    _card_deck: CardDeck
    _state: GameState
    _player_count: int
    _user_interface: UserInterface

    def __init__(self, min_bet: int, initial_chip_count: int):

        self._pot = 0
        self._min_bet = min_bet
        self._current_bet = 0
        self._current_player_index = 0
        self._main_player_index = 0
        self._message = ''
        self._communitary_cards = []
        self._card_deck = CardDeck()
        self._player_count = 0
        self._user_interface = UserInterface()

        seed(time_ns())

        while True:

            self._user_interface.build_menu_interface()

            try:

                self._player_count = int(input(">>> Escolha o número de jogadores (2 a 10): "))
            except ValueError:

                print(">>> Valor inválido (somente números inteiros são permitidos).")
                input(">>> Pressione qualquer tecla para continuar...")
                continue

            if self._player_count >= 2 and self._player_count <= 10:

                break
            else:

                print(">>> Número de jogadores inválido, insira um novo número.")
                input(">>> Pressione qualquer tecla para continuar...")

        self._players_list = [None] * self._player_count
        self._main_player_index = randint(0, self._player_count - 1)

        self._players_list[self._main_player_index] = Player(initial_chip_count, "Você")

        for i in range(self._player_count):

            if self._players_list[i] is None:

                self._players_list[i] = Bot(initial_chip_count, f"Jogador {i + 1}")

        print(f">>> Jogo de {self._player_count} jogadores e 2 fichas de aposta mínima definido.")
        input(">>> Pressione qualquer tecla para continuar...")

        self._state = GameState.INIT

    def get_state(self) -> GameState:

        '''
        Retorna o estado interno do jogo
        '''

        return self._state

    def hand_behaviour(self):

        '''
        Comportamento entre mãos de poker e estados
        '''

        if self._state == GameState.INIT:

            self._message = ">>> Vez do small blind."
            self._state = GameState.SMALL_BLIND
        elif self._state == GameState.SMALL_BLIND:

            self._message = ">>> Vez do big blind."
            self._state = GameState.BIG_BLIND
        elif self._state == GameState.BIG_BLIND:

            for player in self._players_list:

                player.receive_cards(self._card_deck.get_cards(2))

            if self._player_count > 2:

                self._message = ">>> Distribuindo duas cartas para cada jogador."

                self._state = GameState.PRE_FLOP
            else:

                self._communitary_cards += self._card_deck.get_cards(3)
                self._message = ">>> Distribuindo duas cartas para cada jogador e três cartas comunitárias."

                self._state = GameState.FLOP
        elif self._state == GameState.PRE_FLOP and self._current_player_index == 0:

            self._current_bet = 0
            self._communitary_cards += self._card_deck.get_cards(3)
            self._message = ">>> Distribuindo três cartas comunitárias."

            self._state = GameState.FLOP
        elif self._state == GameState.FLOP and self._current_player_index == 0:

            self._current_bet = 0
            self._communitary_cards += self._card_deck.get_cards(1)
            self._message = ">>> Distribuindo a quarta carta comunitária."

            self._state = GameState.TURN
        elif self._state == GameState.TURN and self._current_player_index == 0:

            self._current_bet = 0
            self._communitary_cards += self._card_deck.get_cards(1)
            self._message = ">>> Distribuindo a quinta carta comunitária."

            self._state = GameState.RIVER
        elif self._state == GameState.RIVER and self._current_player_index == 0:

            for player in self._players_list:

                player.set_hand_level(self.hand_level_calc(player, self._communitary_cards))

            sorted_players = sorted(self._players_list, key = lambda player: player.get_hand_level(), reverse = True)

            self._players_list = self._players_list[1:] + self._players_list[:1] # Passa o primeiro jogador para o final da lista

            self._message = ">>> Comparando."
            self._state = GameState.COMP

            self._user_interface.build_turnover_interface(sorted_players, self._communitary_cards, self._player_count, self._pot)
            input(">>> Pressione qualquer tecla para continuar...")

    def player_behaviour(self):

        '''
        Controla as jogadas para os jogadores
        '''

        self._user_interface.build_game_interface(self._players_list,
                                                  self._communitary_cards,
                                                  self._player_count,
                                                  self._pot,
                                                  self._main_player_index,
                                                  self._current_player_index,
                                                  self._message)

        if self._players_list[self._current_player_index].is_active():

            self._players_list[self._current_player_index].set_hand_level(self.hand_level_calc(self._players_list[self._current_player_index],
                                                                                               self._communitary_cards))

            player_result = self._players_list[self._current_player_index].behaviour(self._min_bet,
                                                                              self._state,
                                                                              self._current_bet,
                                                                              self._communitary_cards)

            if player_result != -1:

                player_last_bet = self._players_list[self._current_player_index].get_last_bet()

                if player_last_bet > 0:

                    self._current_bet = player_last_bet
                self._pot += player_result
            elif self._current_player_index == self._main_player_index:

                print(">>> Fim de jogo, você perdeu")
                self._state = GameState.FINISHED
            else:

                self._pot += self._players_list[self._current_player_index].drop_chips()
                self._card_deck.give_cards(self._players_list[self._current_player_index].drop_cards())
                self._players_list.remove(self._players_list[self._current_player_index])
                self._current_player_index -= 1
                self._player_count -= 1

                self.update_main_player_index()

            if self._player_count == 1:

                self._state = GameState.FINISHED
                self._user_interface.build_gameover_interface(self._players_list)

            if self._state == GameState.FINISHED:

                answer = ''

                while True:

                    answer = input(">>> Deseja jogar novamente? (s/n): ")

                    if answer not in ['s', 'n']:

                        print(">>> Resposta inválida.")
                    else:

                        if answer == 'n':

                            self._state = GameState.EXITING

                        break

            input(">>> Pressione qualquer tecla para continuar...")

        self._current_player_index += 1

        if self._current_player_index > self._player_count - 1:

            self._current_player_index = 0

    def restore_game(self):

        '''
        Restora o jogo para uma nova rodada
        '''

        sorted_players = sorted(self._players_list, key = lambda player: player.get_hand_level(), reverse = True)
        sorted_players[0].give_chips(self._pot)
        self._pot = 0
        self._current_bet = 0
        self._current_player_index = 0

        self.update_main_player_index()

        for i in range(self._player_count):

            self._players_list[i].restore_player()
            self._card_deck.give_cards(self._players_list[i].drop_cards())

        self._card_deck.give_cards(self._communitary_cards.copy())
        self._communitary_cards = []

        if self._state != GameState.FINISHED and self._state != GameState.EXITING:

            self._state = GameState.INIT

    def hand_level_calc(self, player, communitary_cards: list) -> float:

        '''
        Calcula o nível da mão e retorna esse nível
        '''

        cards_list = player.get_card_list() + communitary_cards

        if player.is_active() and len(cards_list) > 0:

            level_list = [0] * 10

            level_list[0] = self.royal_flush_check(cards_list)
            level_list[1] = self.straight_flush_check(cards_list)
            level_list[2] = self.four_of_a_kind_check(cards_list)
            level_list[3] = self.full_house_check(cards_list)
            level_list[4] = self.flush_check(cards_list)
            level_list[5] = self.straight_check(cards_list)
            level_list[6] = self.three_of_a_kind_check(cards_list)
            level_list[7] = self.two_pair_check(cards_list)
            level_list[8] = self.pair_check(cards_list)
            level_list[9] = self.high_card_check(cards_list)

            return max(level_list)
        else:

            return 0.0

    def update_main_player_index(self):

        '''
        Atualiza o índice do jogador na lista de jogadores
        '''

        for i in range(len(self._players_list)):

            if self._players_list[i].get_name() == "Você":

                self._main_player_index = i

    def royal_flush_check(self, card_list: list) -> float:

        '''
        Checa se as cartas formam um royal flush
        '''

        royal_flush = ["Ás", "Rei", "Rainha", "Valete", "10"]

        suit_list = [[], [], [], []]

        comp_list = [0] * 4

        for c in card_list:

            if c.get_suit() == "Paus":

                suit_list[0].append(c)
            elif c.get_suit() == "Ouros":

                suit_list[1].append(c)
            elif c.get_suit() == "Copas":

                suit_list[2].append(c)
            else:

                suit_list[3].append(c)

        for i in range(4):

            for c in suit_list[i]:

                if c.get_rank() in royal_flush:

                    comp_list[i] += 1

        if max(comp_list) == 5:

            return 10.0
        else:

            return 0.0

    def straight_flush_check(self, card_list: list) -> float:

        '''
        Checa se as cartas formam um straight flush
        '''

        suit_list = [[], [], [], []]
        rank_list = [[], [], [], []]

        comp_list = [0] * 4

        for c in card_list:

            if c.get_suit() == "Paus":

                suit_list[0].append(c)
            elif c.get_suit() == "Ouros":

                suit_list[1].append(c)
            elif c.get_suit() == "Copas":

                suit_list[2].append(c)
            else:

                suit_list[3].append(c)

        for i in range(4):

            suit_list[i].sort(key = lambda card: card.get_rank(True))

            for j in range(len(suit_list[i]) - 1):

                diff = suit_list[i][j + 1].get_rank(True) - suit_list[i][j].get_rank(True)

                if diff == 1:

                    if comp_list[i] != 0:

                        comp_list[i] += 1
                        rank_list[i].append(suit_list[i][j + 1].get_rank(True))
                    else:

                        comp_list[i] += 2
                        rank_list[i].append(suit_list[i][j].get_rank(True))
                        rank_list[i].append(suit_list[i][j + 1].get_rank(True))

                    if comp_list[i] >= 5:

                        break
                elif diff != 0:

                    comp_list[i] = 0

        max_straight = max(comp_list)
        index = comp_list.index(max_straight)

        if max_straight >= 5:

            return 9.0 + max(rank_list[index]) / 14.0
        else:

            return 0.0

    def four_of_a_kind_check(self, card_list: list) -> float:

        '''
        Checa se as cartas formam uma quadra
        '''

        comp_dict = {}

        for c in card_list:

            if c.get_rank() not in comp_dict.keys():

                comp_dict[c.get_rank()] = 1
            else:

                comp_dict[c.get_rank()] += 1

        values = list(comp_dict.values())
        keys = list(comp_dict.keys())

        max_4 = max(values)
        max_4_rank = keys[values.index(max_4)]

        if max_4 == 4:

            return 8.0 + self._card_deck.rank_to_value(max_4_rank) / 14.0
        else:

            return 0.0

    def full_house_check(self, card_list: int) -> float:

        '''
        Checa se as cartas formam uma full house
        '''

        comp_dict = {}
        rank_list = []

        for c in card_list:

            if c.get_rank() not in comp_dict.keys():

                comp_dict[c.get_rank()] = 1
            else:

                comp_dict[c.get_rank()] += 1

        has_3 = False
        has_2 = False

        values = list(comp_dict.values())
        keys = list(comp_dict.keys())

        for i in range(len(values)):

            if values[i] >= 3 and not has_3:

                has_3 = True
                rank_list.append(self._card_deck.rank_to_value(keys[i]))
            elif values[i] >= 2 and not has_2:

                has_2 = True
                rank_list.append(self._card_deck.rank_to_value(keys[i]))

        if has_3 and has_2:

            return 7.0 + max(rank_list) / 14.0
        else:

            return 0.0

    def flush_check(self, card_list: list) -> float:

        '''
        Checa se as cartas formam um flush
        '''

        comp_dict = {}
        rank_list = []

        for c in card_list:

            if c.get_suit() not in comp_dict.keys():

                comp_dict[c.get_suit()] = 1
            else:

                comp_dict[c.get_suit()] += 1

        values = list(comp_dict.values())
        keys = list(comp_dict.keys())

        max_flush = max(values)
        max_flush_suit = keys[values.index(max_flush)]

        for c in card_list:

            if c.get_suit() == max_flush_suit:

                rank_list.append(c.get_rank(True))

        if max_flush >= 5:

            return 6.0 + max(rank_list) / 14.0
        else:

            return 0.0

    def straight_check(self, card_list: list) -> float:

        '''
        Checa se as cartas formam uma sequência
        '''

        card_list.sort(key = lambda card: card.get_rank(True))
        rank_list = []
        comp = 0

        for i in range(len(card_list) - 1):

            diff = card_list[i + 1].get_rank(True) - card_list[i].get_rank(True)

            if diff == 1:

                if comp != 0:

                    comp += 1
                    rank_list.append(card_list[i + 1].get_rank(True))
                else:

                    comp += 2
                    rank_list.append(card_list[i].get_rank(True))
                    rank_list.append(card_list[i + 1].get_rank(True))

                if comp >= 5:

                    break
            elif diff != 0:

                comp = 0

        if comp >= 5:

            return 5.0 + max(rank_list) / 14.0
        else:

            return 0.0

    def three_of_a_kind_check(self, card_list: list) -> float:

        '''
        Checa se as cartas formam uma trinca
        '''

        comp_dict = {}

        for c in card_list:

            if c.get_rank() not in comp_dict.keys():

                comp_dict[c.get_rank()] = 1
            else:

                comp_dict[c.get_rank()] += 1

        values = list(comp_dict.values())
        keys = list(comp_dict.keys())

        has_3_int_rank = self._card_deck.rank_to_value(keys[values.index(max(values))])

        if max(values) >= 3:

            return 4.0 + has_3_int_rank / 14.0
        else:

            return 0.0

    def two_pair_check(self, card_list: list) -> float:

        '''
        Checa se as cartas formam dois pares
        '''

        comp_dict = {}
        rank_list = []

        for c in card_list:

            if c.get_rank() not in comp_dict.keys():

                comp_dict[c.get_rank()] = 1
            else:

                comp_dict[c.get_rank()] += 1

        values = list(comp_dict.values())
        keys = list(comp_dict.keys())

        pairs = 0

        for i in range(len(values)):

            if values[i] >= 2:

                pairs += 1
                rank_list.append(self._card_deck.rank_to_value(keys[i]))

        if pairs >= 2:

            return 3.0 + max(rank_list) / 14.0
        else:

            return 0.0

    def pair_check(self, card_list: list) -> float:

        '''
        Checa se as cartas formam um par
        '''

        comp_dict = {}

        for c in card_list:

            if c.get_rank() not in comp_dict.keys():

                comp_dict[c.get_rank()] = 1
            else:

                comp_dict[c.get_rank()] += 1

        values = list(comp_dict.values())
        keys = list(comp_dict.keys())

        pairs = 0
        rank_value = 0

        for i in range(len(values)):

            if values[i] >= 2:

                pairs = 1
                rank_value = self._card_deck.rank_to_value(keys[i])
                break

        if pairs == 1:

            return 2.0 + rank_value / 14.0
        else:

            return 0.0

    def high_card_check(self, card_list: list) -> float:

        '''
        Retorna o nível da mão equivalente a carta mais alta
        '''

        rank_list = []

        for c in card_list:

            rank_list.append(c.get_rank(True))

        return max(rank_list) / 14.0
