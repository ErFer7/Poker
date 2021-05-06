# -*- coding: utf-8 -*-

'''
Módulo para a implementação das cartas e do baralho
'''

from random import choice

class CardDeck():

    '''
    Esta classe descreve o baralho
    '''

    _card_list: list

    def __init__(self):

        self._card_list = []

        # Geração do baralho
        # Cada carta é gerada e depois é atribuída a algum naipe

        suit = ''

        for i in range(4):

            if i == 0:

                suit = "Paus"
            elif i == 1:

                suit = "Ouros"
            elif i == 2:

                suit = "Copas"
            else:

                suit = "Espadas"

            self._card_list += [Card('2', 1, suit),
                                Card('3', 2, suit),
                                Card('4', 3, suit),
                                Card('5', 4, suit),
                                Card('6', 5, suit),
                                Card('7', 6, suit),
                                Card('8', 7, suit),
                                Card('9', 8, suit),
                                Card("10", 9, suit),
                                Card("Valete", 10, suit),
                                Card("Rainha", 11, suit),
                                Card("Rei", 12, suit),
                                Card("Ás", 13, suit)]

    def get_cards(self, ammout: int) -> list:

        '''
        Distribui cartas embaralhadas
        '''

        cards = []

        for _ in range(ammout):

            cards.append(choice(self._card_list))
            self._card_list.remove(cards[-1])

        return cards

    def give_cards(self, cards: list):

        '''
        Recebe cartas de volta
        '''

        self._card_list += cards

    def rank_to_value(self, rank: str) -> int:

        '''
        Converte o ranque de string para int
        '''

        value = 0

        if rank == "Ás":

            value = 13
        elif rank == "Rei":

            value = 12
        elif rank == "Rainha":

            value = 11
        elif rank == "Valete":

            value = 10
        elif rank == "10":

            value = 9
        elif rank == "9":

            value = 8
        elif rank == "8":

            value = 7
        elif rank == "7":

            value = 6
        elif rank == "6":

            value = 5
        elif rank == "5":

            value = 4
        elif rank == "4":

            value = 3
        elif rank == "3":

            value = 2
        else:

            value = 1

        return value

class Card():

    '''
    Descreve uma carta
    '''

    _rank: str
    _value: int
    _suit: str

    def __init__(self, rank: str, val: int, suit: str):

        self._rank = rank
        self._value = val
        self._suit = suit

    def __repr__(self) -> str:

        return f"{self._rank} de {self._suit}"

    def get_rank(self, int_value: bool = False):

        '''
        Retorna o ranque da carta. Pode ser um string ou int
        '''

        if int_value:

            return self._value
        else:

            return self._rank

    def get_suit(self) -> str:

        '''
        Retorna o naipe
        '''

        return self._suit
