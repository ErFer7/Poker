# -*- coding: utf-8 -*-

'''
Módulo com as classes que definem os jogadores
'''

from abc import ABC, abstractclassmethod
from random import randint, uniform

from states import GameState

class Person(ABC):

    '''
    Classe abstrata que define uma pessoa
    '''

    _player_id: str
    _chips: int
    _card_list: list
    _active: bool
    _last_bet: int
    _hand_level: float

    def __init__(self, initial_chip_count: int, player_id: str):

        super().__init__()

        self._player_id = player_id
        self._chips = initial_chip_count
        self._card_list = []
        self._active = True
        self._last_bet = 0
        self._hand_level = 0.0

    @abstractclassmethod
    def get_name(cls) -> str:

        '''
        Retorna o nome
        '''

    @abstractclassmethod
    def get_chips(cls) -> int:

        '''
        Retorna as fichas
        '''

    @abstractclassmethod
    def give_chips(cls, chips: int):

        '''
        Entrega fichas ao jogador
        '''

    @abstractclassmethod
    def get_card_list(cls) -> list:

        '''
        Retorna lista de cartas
        '''

    @abstractclassmethod
    def is_active(cls) -> bool:

        '''
        Retorna um valor booleano que determina se o jogador está ativo ou não
        '''

    @abstractclassmethod
    def get_hand_level(cls) -> float:

        '''
        Retorna a nível da mão
        '''

    @abstractclassmethod
    def set_hand_level(cls, level: float):

        '''
        Define o nível da mão
        '''

    @abstractclassmethod
    def restore_player(cls):

        '''
        Define o jogador como ativo
        '''

    @abstractclassmethod
    def get_last_bet(cls) -> int:

        '''
        Retorna a última aposta
        '''

    @abstractclassmethod
    def small_blind(cls, min_bet: int) -> int:

        '''
        Define como a small blind é jogada
        '''

    @abstractclassmethod
    def big_blind(cls, min_bet: int) -> int:

        '''
        Define como a big blind é jogada
        '''

    @abstractclassmethod
    def pay(cls, previous_bet: int) -> int:

        '''
        Cobre uma aposta
        '''

    @abstractclassmethod
    def fold(cls) -> int:

        '''
        Desiste
        '''

    @abstractclassmethod
    def raise_bet(cls, min_bet: int, previous_bet: int) -> int:

        '''
        Aumenta uma aposta
        '''

    @abstractclassmethod
    def bet(cls, min_bet: int) -> int:

        '''
        Aposta
        '''

    @abstractclassmethod
    def skip(cls) -> int:

        '''
        Passa a vez
        '''

    @abstractclassmethod
    def behaviour(cls, min_bet: int, state: GameState, previous_bet: int, communitary_cards: list) -> int:

        '''
        Comportamento
        '''

    @abstractclassmethod
    def receive_cards(cls, cards: list):

        '''
        Recebe cartas
        '''

    @abstractclassmethod
    def drop_chips(cls) -> int:

        '''
        Entrega todas fichas
        '''

    @abstractclassmethod
    def drop_cards(cls) -> list:

        '''
        Entrega todas cartas
        '''

class Player(Person):

    '''
    Classe que descreve o jogador (usuário)
    '''

    def __init__(self, initial_chip_count: int, player_id: str):

        super().__init__(initial_chip_count, player_id)

    def get_name(self) -> str:

        return self._player_id

    def get_chips(self) -> int:

        return self._chips

    def give_chips(self, chips: int):

        self._chips += chips

    def get_card_list(self) -> list:

        return self._card_list

    def is_active(self) -> bool:

        return self._active

    def get_hand_level(self) -> float:

        return self._hand_level

    def set_hand_level(self, level: float):

        self._hand_level = level

    def restore_player(self):

        self._hand_level = 0
        self._last_bet = 0
        self._active = True

    def get_last_bet(self) -> int:

        return self._last_bet

    def small_blind(self, min_bet: int) -> int:

        chips = 0

        if self._chips >= min_bet // 2:

            self._chips -= min_bet // 2
            chips = min_bet // 2
            self._last_bet = chips
            print(f">>> Você é o small blind e teve que pagar {min_bet // 2} fichas.")
        else:

            chips = -1
            print(f">>> Você é o small blind e não tem {min_bet // 2} fichas para pagar. Você foi eliminado.")

        return chips

    def big_blind(self, min_bet: int) -> int:

        chips = 0

        if self._chips >= min_bet:

            self._chips -= min_bet
            chips = min_bet
            self._last_bet = chips
            print(f">>> Você é o big blind e teve que pagar {min_bet} fichas")
        else:

            chips = -1
            print(f">>> Você é o bit blind e não tem {min_bet} fichas para pagar. Você foi eliminado.")

        return chips

    def pay(self, previous_bet: int) -> int:

        if self._chips >= previous_bet:

            self._chips -= previous_bet
            self._last_bet = previous_bet
            print(f">>> Você cobriu a aposta de {previous_bet} fichas")
            return previous_bet
        else:

            print(f">>> Você não tem fichas para cobrir a aposta de {previous_bet} fichas. :(")

            return -1

    def fold(self) -> int:

        if self._chips > 0:

            print(">>> Você desistiu nesta rodada.")
            self._active = False
            return 0
        else:

            print(">>> Você não pode desistir com nenhuma ficha. Você perdeu.")
            return -1

    def raise_bet(self, min_bet: int, previous_bet: int) -> int:

        chips = 0

        if self._chips >= previous_bet + min_bet:

            while True:

                try:

                    chips = int(input(f">>> Insira um valor para adicionar a sua aposta ({min_bet} <= valor <= {self._chips - previous_bet}): "))

                    if chips < min_bet or chips > self._chips - previous_bet:

                        raise ValueError
                except ValueError:

                    print(f">>> Dados incorretos. Insira um número inteiro no intervalo [{min_bet} <= valor <= {self._chips - previous_bet}].")
                    continue

                break
        else:

            print(">>> Você não tem fichas suficientes para aumentar a sua aposta e deve tentar outra opção.")
            return 0

        self._chips -= previous_bet + chips
        print(f">>> Você apostou {previous_bet + chips} fichas. ({previous_bet} + {chips})")
        self._last_bet += previous_bet + chips

        return previous_bet + chips

    def bet(self, min_bet: int) -> int:

        chips = 0

        if self._chips >= min_bet:

            while True:

                try:

                    chips = int(input(f">>> Insira um valor para a sua aposta (mínimo: {min_bet}): "))

                    if chips < min_bet or chips > self._chips:

                        raise ValueError
                except ValueError:

                    print(f">>> Dados incorretos. Insira um número inteiro no intervalo [{min_bet} <= valor <= {self._chips}].")
                    continue

                break
        else:

            print(">>> Você não possui fichas para continuar no jogo :(")
            return -1

        self._chips -= chips
        print(f">>> Você apostou {chips} fichas.")
        self._last_bet = chips

        return chips

    def skip(self) -> int:

        if self._chips > 0:

            self._last_bet = 0
            print(">>> Você passou a vez.")
            return 0
        else:

            print(">>> Você não tem fichas e não pode continuar no jogo.")
            return -1

    def behaviour(self, min_bet: int, state: GameState, previous_bet: int, communitary_cards: list) -> int:

        behav_chips = 0

        if state == GameState.SMALL_BLIND:

            self.small_blind(min_bet)
        elif state == GameState.BIG_BLIND:

            self.big_blind(min_bet)
        else:

            if previous_bet > 0:

                print(f">>> Escolha entre pagar a aposta , desistir ou aumentar a aposta. (Valor da aposta: {previous_bet} fichas)")
            else:

                print(">>> Escolha entre apostar, desistir ou passar a vez.")

            while True:

                if previous_bet > 0:

                    action = input(">>> Digite [pagar], [desistir] ou [aumentar] para continuar: ")

                    if action == "pagar":

                        behav_chips = self.pay(previous_bet)
                        break
                    elif action == "desistir":

                        behav_chips = self.fold()
                        break
                    elif action == "aumentar":

                        behav_chips = self.raise_bet(min_bet, previous_bet)

                        if behav_chips > 0:

                            break
                    else:

                        print(">>> Comando não reconhecido. tente novamente.")
                else:

                    action = input(">>> Digite [apostar], [desistir] ou [passar] para continuar: ")

                    if action == "apostar":

                        behav_chips = self.bet(min_bet)
                        break
                    elif action == "desistir":

                        behav_chips = self.fold()
                        break
                    elif action == "passar":

                        behav_chips = self.skip()
                        break
                    else:

                        print(">>> Comando não reconhecido. tente novamente.")

        return behav_chips

    def receive_cards(self, cards: list):

        self._card_list += cards

    def drop_chips(self) -> int:

        chips = self._chips
        self._chips = 0
        return chips

    def drop_cards(self) -> list:

        cards = self._card_list.copy()
        self._card_list = []
        return cards

class Bot(Person):

    '''
    O jogador armazena as suas cartas
    '''

    _action_coeff: float

    def __init__(self, initial_chip_count: int, player_id: str):

        super().__init__(initial_chip_count, player_id)

        self._action_coeff = uniform(0.5, 1.0)

    def get_name(self) -> str:

        return self._player_id

    def get_chips(self) -> int:

        return self._chips

    def give_chips(self, chips: int):

        self._chips += chips

    def get_card_list(self) -> list:

        return self._card_list

    def is_active(self) -> bool:

        return self._active

    def get_hand_level(self) -> float:

        return self._hand_level

    def set_hand_level(self, level: float):

        self._hand_level = level

    def restore_player(self):

        self._hand_level = 0
        self._last_bet = 0
        self._active = True

    def get_last_bet(self) -> int:

        return self._last_bet

    def small_blind(self, min_bet: int) -> int:

        chips = 0

        if self._chips >= min_bet // 2:

            self._chips -= min_bet // 2
            chips = min_bet // 2
            self._last_bet = chips
            print(f">>> {self._player_id} é o small blind e teve que pagar {min_bet // 2} fichas.")
        else:

            chips = -1
            print(f">>> {self._player_id} é o small blind e não tem {min_bet // 2} fichas para pagar. Jogador eliminado.")

        return chips

    def big_blind(self, min_bet: int) -> int:

        chips = 0

        if self._chips >= min_bet:

            self._chips -= min_bet
            chips = min_bet
            self._last_bet = chips
            print(f">>> {self._player_id} é o big blind e teve que pagar {min_bet} fichas.")
        else:

            chips = -1
            print(f">>> {self._player_id} é o big blind e não tem {min_bet // 2} fichas para pagar. Jogador eliminado.")

        return chips

    def pay(self, previous_bet: int) -> int:

        if self._chips >= previous_bet:

            self._chips -= previous_bet
            self._last_bet = previous_bet
            print(f">>> {self._player_id} cobriu a aposta de {previous_bet} fichas.")
            return previous_bet
        else:

            print(f">>> {self._player_id} não tem fichas para cobrir a aposta de {previous_bet} fichas. O jogador foi eliminado.")

            return -1

    def fold(self) -> int:

        if self._chips > 0:

            print(f">>> {self._player_id} desistiu nesta rodada.")
            self._active = False
            return 0
        else:

            print(f">>> {self._player_id} não tem fichas e foi eliminado.")
            return -1

    def raise_bet(self, min_bet: int, previous_bet: int) -> int:

        chips = 0
        max_bet = int(self._chips * self._action_coeff * uniform(0.0, 0.05))

        if max_bet < min_bet:

            chips = min_bet
        else:

            chips = randint(min_bet, max_bet)

        self._chips -= previous_bet + chips
        print(f">>> {self._player_id} apostou {previous_bet + chips} fichas. ({previous_bet} + {chips})")
        self._last_bet += previous_bet + chips

        return previous_bet + chips

    def bet(self, min_bet: int) -> int:

        if self._chips >= min_bet:

            chips = 0
            max_bet = int(self._chips * self._action_coeff * uniform(0.0, 0.05))

            if max_bet < min_bet:

                chips = min_bet
            else:

                chips = randint(min_bet, max_bet)

            if chips > self._chips:

                chips = self._chips

            self._chips -= chips
            print(f">>> {self._player_id} apostou {chips} fichas.")
            self._last_bet = chips

            return chips
        else:

            print(f">>> {self._player_id} não tem fichas para continuar no jogo.")
            return -1

    def skip(self) -> int:

        if self._chips > 0:

            self._last_bet = 0
            print(f">>> {self._player_id} passou a vez.")
            return 0
        else:

            print(f">>> {self._player_id} não tinha fichas e não podia continuar no jogo.")
            return -1

    def behaviour(self, min_bet: int, state: GameState, previous_bet: int, communitary_cards: list) -> int:

        behav_chips = 0

        if state == GameState.SMALL_BLIND:

            self.small_blind(min_bet)
        elif state == GameState.BIG_BLIND:

            self.big_blind(min_bet)
        else:

            if len(communitary_cards) > 0:

                action_value = self._hand_level * self._action_coeff
            else:

                action_value = uniform(5.0, 10.0) * self._action_coeff

            if previous_bet > 0:

                if self._chips >= previous_bet + min_bet:

                    if action_value <= 0.3:

                        behav_chips = self.fold()
                    elif action_value <= 4.0:

                        behav_chips = self.pay(previous_bet)
                    else:

                        behav_chips = self.raise_bet(min_bet, previous_bet)
                else:

                    if action_value <= 0.3:

                        behav_chips = self.fold()
                    else:

                        behav_chips = self.pay(previous_bet)
            else:

                if action_value <= 0.3:

                    behav_chips = self.fold()
                elif action_value <= 2.0:

                    behav_chips = self.skip()
                else:

                    behav_chips = self.bet(min_bet)

        return behav_chips

    def receive_cards(self, cards: list):

        self._card_list += cards

    def drop_chips(self) -> int:

        chips = self._chips
        self._chips = 0
        return chips

    def drop_cards(self) -> list:

        cards = self._card_list.copy()
        self._card_list = []
        return cards
