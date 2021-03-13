import random
from itertools import combinations
import time

class Card(object):
    colors = ['kőr', 'treff', 'pikk', 'káró']
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    def __init__(self, color, value):
        self.color = Card.colors.index(color)
        self.value = Card.values.index(value)

    def print(self):
        text = str(Card.colors[self.color]) + ' ' + str(Card.values[self.value])
        print(text)

    def sameColor(self, card):
        sameColor = False
        if self.color == card.color:
            sameColor = True
        return sameColor

    def sameValue(self, card):
        sameValue = False
        if self.value == card.value:
            sameValue = True
        return sameValue

    def same(self, card):
        same = False
        if self.sameColor(card) == True and self.sameValue(card) == True:
            same = True
        return same

class Cards(object):
    def __init__(self):
        self.cards = []
        for i in range(len(Card.colors)):
            for j in range(len(Card.values)):
                card = Card(Card.colors[i], Card.values[j])
                self.cards.append(card)

    def print(self):
        for card in self.cards:
            card.print()

    def shuffle(self):
        random.shuffle(self.cards)

    def pick(self):
        card = self.cards[0]
        #self.cards.remove(card)
        return card

    def remove(self, card):
        if isinstance(card, Card):
            self.cards.remove(card)
        else:
            print('not Card object')

class Deck(Cards):
    numberOfCards = 52
    def __init__(self):
        super().__init__()

class Hand(Cards):
    ranks = ['highCard', 'onePair', 'twoPair', 'three', 'straight', 'flush', 'fullHouse', 'four', 'straightFlush', 'five']
    def __init__(self, cards):
        super().__init__() #cards is a list of Card objects
        self.cards = cards
        self.colors = [card.color for card in cards]
        self.values = [card.value for card in cards]
        self.rank = 0 #highCard

    def ranking(self):
        self.rank = {'rank' : 0, 'value' : 0, 'highCard' : 0}
        if self.five()[0] == True:
            self.rank['rank'] = 9
            self.rank['value'] = self.five()[1]
            self.rank['highCard'] = self.rank['value']
        elif self.straightFlush()[0] == True:
            self.rank['rank'] = 8
            self.rank['value'] = self.straightFlush()[1]
            self.rank['highCard'] = self.rank['value']
        elif self.four()[0] == True:
            self.rank['rank'] = 7
            self.rank['value'] = self.four()[1]
            self.rank['highCard'] = self.four()[2]
        elif self.fullHouse()[0] == True:
            self.rank['rank'] = 6
            self.rank['value'] = max(self.fullHouse()[1])
            self.rank['highCard'] = min(self.fullHouse()[1])
        elif self.flush()[0] == True:
            self.rank['rank'] = 5
            self.rank['value'] = self.flush()[1]
            self.rank['highCard'] = self.flush()[2]
        elif self.straight()[0] == True:
            self.rank['rank'] = 4
            self.rank['value'] = self.straight()[1]
            self.rank['highCard'] = self.straight()[2]
        elif self.three()[0] == True:
            self.rank['rank'] = 3
            self.rank['value'] = self.three()[1]
            self.rank['highCard'] = self.three()[2]
        elif self.twoPair()[0][0] == True:
            self.rank['rank'] = 2
            self.rank['value'] = max(self.twoPair()[0][1])
            self.rank['highCard'] = self.twoPair()[1]
        elif self.onePair()[0][0] == True:
            self.rank['rank'] = 1
            self.rank['value'] = self.onePair()[0][1]
            self.rank['highCard'] = self.onePair()[2]
        else:
            self.rank['rank'] = 0
            self.rank['value'] = self.highCard()[1]
            self.rank['highCard'] = self.rank['value']
        return self.rank

    def sameColors(self, n):
        counter = {cards.color : 0 for cards in self.cards}
        for cards in self.cards:
            counter[cards.color] += 1
        #print(counter)
        sameOnes, sameCards = [], []
        for key, value in counter.items():
            if value == n:
                sameOnes.append(key)
                cards = []
                for card in self.cards:
                    if card.color == key:
                        cards.append(card)
                sameCards.append(cards)
        return sameOnes, sameCards

    def sameValues(self, n):
        counter = {cards.value : 0 for cards in self.cards}
        for cards in self.cards:
            counter[cards.value] += 1
        #print(counter)
        sameOnes, sameCards = [], []
        for key, value in counter.items():
            if value == n:
                sameOnes.append(key)
                cards = []
                for card in self.cards:
                    if card.value == key:
                        cards.append(card)
                sameCards.append(cards)
        return sameOnes, sameCards
        
    def highCard(self):
        highCard, highCardValue, highCardCard = True, -1, ''
        for card in self.cards:
            if card.value > highCardValue:
                highCardValue = card.value
                highCardCard = card
        return highCard, highCardValue, highCardCard

    def onePair(self):
        onePair, onePairValue, onePairCards, highCardValue = False, -1, [], -1
        same2Ones = self.sameValues(2)
        same3Ones = self.sameValues(3)
        if len(same2Ones[0]) == 1 and len(same3Ones[0]) == 0:
            onePair, onePairValue, onePairCards, highCardValue = True, same2Ones[0], same2Ones[1], -1
        return onePair, onePairValue, onePairCards, highCardValue

    def twoPair(self):
        twoPair, twoPairValue, twoPairCards, highCardValue = False, [-1, -1], [], -1
        same2Ones = self.sameValues(2)
        same3Ones = self.sameValues(3)
        if len(same2Ones[0]) == 2 and len(same3Ones[0]) == 0:
            twoPair, twoPairValue, twoPairCards, highCardValue = True, same2Ones[0], [], -1
        return twoPair, twoPairValue, twoPairCards, highCardValue

    def three(self):
        three, threeValue, threeCards, highCardValue = False, -1, [], -1
        same2Ones = self.sameValues(2)
        same3Ones = self.sameValues(3)
        if len(same3Ones[0]) == 1 and len(same2Ones[0]) == 0:
            three, threeValue, threeCards, highCardValue = True, same3Ones[0][0], same3Ones[1], -1
        return three, threeValue, threeCards, highCardValue

    def straight(self):
        straight, straightValue, highCardValue = True, -1, -1
        values = [card.value for card in self.cards]
        values.sort()
        straightValue = values[4]
        i = 0
        while i < 4:
            if values[i+1] - values[i] != 1:
                straight, straightValue, highCardValue = False, -1, -1
                break
            i += 1
        highCardValue = self.highCard()[1]
        return straight, straightValue, highCardValue

    def flush(self):
        flush, flushColor, highCardValue = False, '', -1
        sameness = self.sameColors(5)
        flush = True if sameness[0] != [] else False
        flushColor = Card.colors[sameness[0][0]] if flush == True else ''
        highCardValue = self.highCard()[1]
        return flush, flushColor, highCardValue

##eddig át vannak nézve a kombinációk, four és straightFlush is
##ranking még nem

    def fullHouse(self):
        fullHouse, fullHouseValue, highCardValue = False, [-1, -1], -1
        N = 2
        cardsToTest = self.cards
        combination = combinations(cardsToTest, N)
        for comb in combination:
            _cardsToTest = Hand(list(cardsToTest))
            _cards = Hand(list(comb))
            onePairNess = _cards.onePair()
            if onePairNess[0][0] == True:
##                fullHouseValue[0] = Card.values.index(onePairNess[0][1])
                fullHouseValue[0] = onePairNess[0][1]
                _cardsToTest.remove(onePairNess[1][0])
                _cardsToTest.remove(onePairNess[1][1])
                threeNess = _cardsToTest.three()
                if threeNess[0] == True:
                    fullHouse = True
                    fullHouseValue[1] = threeNess[1]
                    highCardValue = fullHouseValue[1]
                    return fullHouse, fullHouseValue, highCardValue
                else:
                    fullHouse, fullHouseValue, highCardValue = False, [-1, -1], -1
        return fullHouse, fullHouseValue, highCardValue

    def four(self):
        '''
        without joker cards the maximum number of same values is 4
        so no other check is required
        '''
        four, fourValue, highCardValue = False, -1, -1
        sameness = self.sameValues(4)
        if sameness[0] != []:
            four = True
            fourValue = sameness[0][0]
            for card in self.cards:
                if card not in sameness[1][0]:
                    highCardValue = card.value
        return four, fourValue, highCardValue

    def straightFlush(self):
        straightFlush, highCard = False, -1
        if self.straight()[0] == True and self.flush()[0] == True:
            straightFlush = True
            highCard = self.highCard()[1]
        return straightFlush, highCard

    def five(self):
        five = False
        sameness = self.sameValues(5)
        if sameness[0] == 5:
            five = True
        return five, self.highCard()[1]

class Game(object):
    def __init__(self):
        self.deck = Deck()

    def print(self):
        self.handA.print()
        self.handB.print()

    def deal(self):
        self.deck.shuffle()
        handa, handb = [], []
        for i in range(5):
            card = self.deck.pick()
            handa.append(card)
            self.deck.remove(card)
            card = self.deck.pick()
            handb.append(card)
            self.deck.remove(card)
        self.handA = Hand(handa)
        self.handB = Hand(handb)
            
    def play(self):
        self.rankA = self.handA.ranking()
        self.rankB = self.handB.ranking()
        rankA, rankB = self.rankA['rank'], self.rankB['rank']
        #print('-----------')
        #print(rankA, rankB)
        self.winner = 'A' if rankA > rankB else ('B' if rankA < rankB else 'draw')
        if self.winner == 'draw':
            rankA, rankB = self.rankA['value'], self.rankB['value']
            #print(rankA, rankB)
            self.winner = 'A' if rankA > rankB else ('B' if rankA < rankB else 'draw')
            if self.winner == 'draw':
                rankA, rankB = self.rankA['highCard'], self.rankB['highCard']
                #print(rankA, rankB)
                self.winner = 'A' if rankA > rankB else ('B' if rankA < rankB else 'draw')

##winners = {'A' : 0, 'B' : 0, 'draw' : 0}
##n = 1000
##start = time.time()
##for i in range(n):
##    game = Game()
##    game.deal()
####    print('----------')
####    game.print()
##    game.play()
##    #print(game.winner)
##    winners[game.winner] += 1
##print(winners)
##end = time.time()
##deltaSum = end - start
##delta = deltaSum / n
##print(delta)

##card = Card('pikk', 'A')
##card.print()
##deck = Deck()
##deck.shuffle()
##deck.print()
##cardTest = deck.pick()
##cardTest.print()
##deck.remove(cardTest)
##deck.print()
##hand = Hand(deck.cards[0:5])
####hand = Hand([Card('kőr', 2), Card('káró', 2), Card('treff', 3), Card('káró', 5), Card('pikk', 4)]) #one pair
##hand = Hand([Card('kőr', 2), Card('káró', 2), Card('treff', 3), Card('káró', 3), Card('pikk', 4)]) #two pair
##hand = Hand([Card('kőr', 2), Card('káró', 2), Card('treff', 2), Card('káró', 5), Card('pikk', 4)]) #three
##hand = Hand([Card('kőr', 2), Card('káró', 3), Card('treff', 4), Card('káró', 5), Card('pikk', 6)]) #straight
##hand = Hand([Card('káró', 'A'), Card('káró', 3), Card('káró', 4), Card('káró', 'K'), Card('káró', 6)]) #flush
##hand = Hand([Card('kőr', 2), Card('káró', 2), Card('treff', 4), Card('káró', 4), Card('pikk', 4)]) #full house
##hand = Hand([Card('kőr', 2), Card('káró', 2), Card('treff', 2), Card('káró', 4), Card('pikk', 2)]) #four
hand = Hand([Card('káró', 2), Card('káró', 3), Card('káró', 4), Card('káró', 5), Card('káró', 6)]) #straightFlush
##hand = Hand([Card('kőr', 2), Card('káró', 2), Card('treff', 2), Card('káró', 4), Card('kőr', 2)]) #five
hand.print()
##print('1 of the same colors', hand.sameColors(1))
##print('2 of the same colors', hand.sameColors(2))
print('5 of the same colors', hand.sameColors(5))
print('1 of the same values', hand.sameValues(1))
##print('2 of the same values', hand.sameValues(2))
##print('3 of the same values', hand.sameValues(3))
##print('5 of the same values', hand.sameValues(5))
##print('Ranking:', hand.ranking()['rank'])
##print('High card?', hand.highCard()[0])
##print('Pair?', hand.onePair()[0])
##print('Two pair?', hand.twoPair())
##print('Three?', hand.three())
##print('Straight?', hand.straight())
##print('Flush?', hand.flush())
##print('Full house?', hand.fullHouse())
print('Four?', hand.four())
print('Straight flush?', hand.straightFlush())
##print('Five?', hand.five())


##deck = Deck()
##deck.shuffle()
##handa, handb = [], []
##for i in range(5):
##    card = deck.pick()
##    handa.append(card)
##    deck.remove(card)
##    card = deck.pick()
##    handb.append(card)
##    deck.remove(card)
##handA = Hand(handa)
##handB = Hand(handb)
####handA = Hand([Card('kőr', 2), Card('káró', 2), Card('treff', 4), Card('káró', 4), Card('pikk', 4)]) #full house, rank 6
####handB = Hand([Card('kőr', 2), Card('káró', 2), Card('treff', 3), Card('káró', 3), Card('pikk', 4)]) #two pair, rank 2
##print('Hand A:')
##handA.print()
##print('\nHand B:')
##handB.print()
##rankA = handA.ranking()
##rankB = handB.ranking()
##print('')
##print('Rank A:', rankA)
##print('Rank B:', rankB)
##print('A wins' if rankA > rankB else ('B wins' if rankA < rankB else 'draw'))


##hand = Hand([Card('kőr', 2), Card('káró', 2), Card('treff', 3), Card('káró', 5), Card('pikk', 4)]) #one pair
##methods = [hand.highCard, hand.onePair, hand.twoPair, hand.three, hand.straight, hand.flush, hand.fullHouse, hand.four, hand.straightFlush, hand.five, ]
##n = 10000
##for method in methods:
##    print(method)
##    start = time.time()
##    try:
##        for i in range(n):
##            method()
##    except:
##        print('except')
##        pass
##    end = time.time()
##    deltaSum = end - start
##    delta = deltaSum / n
##    print(delta)
