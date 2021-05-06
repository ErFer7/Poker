from random import choice

'''
Usei inglês para padronizar o código.

As cartas poderiam ser embaralhadas durante a sua distribuição, porém tentei deixar
cada passo isolado um do outro.

Feito em python 3.9.1
'''

class Deck():

    '''
    Esta classe descreve o baralho
    '''

    _card_list: list

    def __init__(self) -> None:

        self._card_list = []

        # Geração do baralho
        # Cada carta é gerada e depois é atribuída a algum naipe

        for i in range(4):

            self._card_list += [Card('A'),
                                Card('2'),
                                Card('3'),
                                Card('4'),
                                Card('5'),
                                Card('6'),
                                Card('7'),
                                Card('8'),
                                Card('9'),
                                Card("10"),
                                Card("Valete"),
                                Card("Rainha"),
                                Card("Rei")]

            if i == 0:

                for j in range(len(self._card_list) - 13, len(self._card_list)):

                    self._card_list[j].card_suit = "Paus"
            elif i == 1:

                for j in range(len(self._card_list) - 13, len(self._card_list)):

                    self._card_list[j].card_suit = "Ouros"
            elif i == 2:
            
                for j in range(len(self._card_list) - 13, len(self._card_list)):
                
                    self._card_list[j].card_suit = "Copas"
            else:
            
                for j in range(len(self._card_list) - 13, len(self._card_list)):
                
                    self._card_list[j].card_suit = "Espadas"
    
    def shuffle(self) -> None:

        '''
        Embaralha as cartas
        '''

        shuffled_list = []

        while len(self._card_list) > 0:

            element = choice(self._card_list)
            shuffled_list += [element]
            self._card_list.remove(element)

        self._card_list = shuffled_list.copy()
    
    def distribute(self, players: list) -> None:

        '''
        A distribuição pode ser inexata quando as cartas não podem ser divididas igualmente entre
        cada jogador
        '''

        # Distribuição inicial
        for i in range(len(players)):

            for j in range(52 // len(players)):

                players[i].receive(self._card_list[j])
                self._card_list.remove(self._card_list[j])

        # Distribuição do resto das cartas
        for i in range(len(players)):

            if len(self._card_list) == 0:
                break

            players[i].receive(self._card_list[0])
            self._card_list.remove(self._card_list[0])

class Card():

    card_type: str
    card_suit: str

    def __init__(self, card_type = None, card_suit = None) -> None:

        self.card_type = card_type
        self.card_suit = card_suit
    
    def __repr__(self) -> str:
        
        return f"{self.card_type} de {self.card_suit}"

    @property
    def card_type(self):

        '''
        Getter do tipo
        '''

        return self._card_type

    @card_type.setter
    def card_type(self, val):

        '''
        Setter do tipo
        '''

        self._card_type = val
    
    @property
    def card_suit(self):

        '''
        Getter do naipe
        '''

        return self._card_suit

    @card_suit.setter
    def card_suit(self, val):

        '''
        Setter do naipe
        '''

        self._card_suit = val
    
class Player():

    '''
    O jogador armazena as suas cartas
    '''

    _card_list: list

    def __init__(self) -> None:
        
        self._card_list = []
    
    def receive(self, card) -> None:

        '''
        Recebe uma carta
        '''

        self._card_list.append(card)
    
    def __repr__(self) -> str:
        
        '''
        Retorna um string com a lista de cartas
        '''
        
        return f"Cartas: {', '.join(map(str, self._card_list))}"

deck = Deck()   # Cria o baralho
deck.shuffle()  # Embaralha o baralho

players = []    # Cria uma lista para os jogadores

for i in range(9):

    players.append(Player())    # Cria um jogador

deck.distribute(players)    # Distribui as cartas para cada jogador

for i in range(9):

    # Resultados
    print(f"Jogador {i + 1}:")
    print(f"{players[i]}\n")