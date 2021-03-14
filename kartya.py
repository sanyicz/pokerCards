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
            self.rank['highCard'] = self.five()[2]
        elif self.straightFlush()[0] == True:
            self.rank['rank'] = 8
            self.rank['value'] = self.straightFlush()[1]
            self.rank['highCard'] = self.straightFlush()[2]
        elif self.four()[0] == True:
            self.rank['rank'] = 7
            self.rank['value'] = self.four()[1]
            self.rank['highCard'] = self.four()[2]
        elif self.fullHouse()[0] == True:
            self.rank['rank'] = 6
            self.rank['value'] = self.fullHouse()[1]
            self.rank['highCard'] = self.fullHouse()[2]
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
        elif self.twoPair()[0] == True:
            self.rank['rank'] = 2
            self.rank['value'] = max(self.twoPair()[1])
            self.rank['highCard'] = self.twoPair()[2]
        elif self.onePair()[0] == True:
            self.rank['rank'] = 1
            self.rank['value'] = self.onePair()[1]
            self.rank['highCard'] = self.onePair()[2]
        else:
            self.rank['rank'] = 0
            self.rank['value'] = self.highCard()[1]
            self.rank['highCard'] = self.highCard()[2]
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
        highCard, highCardValue, highCardList = True, -1, []
        for card in self.cards:
            highCardList.append(card.value)
        highCardList.sort(reverse=True)
        highCardValue = highCardList[0] #max(highCardList)
        return highCard, highCardValue, highCardList

    def onePair(self):
        onePair, onePairValue, onePairCards, highCardList = False, -1, [], []
        same2Ones = self.sameValues(2)
        same3Ones = self.sameValues(3)
        if len(same2Ones[0]) == 1 and len(same3Ones[0]) == 0:
            onePair, onePairValue, onePairCards, highCardList = True, same2Ones[0], same2Ones[1], []
            for card in self.cards:
                for onePairCard in onePairCards[0]:
                    if card.value != onePairCard.value and card.value not in highCardList:
                        highCardList.append(card.value)
            highCardList.sort(reverse=True)
        return onePair, onePairValue, highCardList, onePairCards

    def twoPair(self):
        twoPair, twoPairValue, twoPairCards, highCardList = False, [-1, -1], [], -1
        same2Ones = self.sameValues(2)
        same3Ones = self.sameValues(3)
        if len(same2Ones[0]) == 2 and len(same3Ones[0]) == 0:
            twoPair, twoPairValue, twoPairCards = True, same2Ones[0], same2Ones[1]
            highCardList = [min(same2Ones[0])]
            for card in self.cards:
                for twoPairCard in twoPairCards[0]:
                    if card.value != twoPairCard.value and card.value not in highCardList:
                        highCardList.append(card.value)
            highCardList.sort(reverse=True)
        return twoPair, twoPairValue, highCardList, twoPairCards

    def three(self):
        three, threeValue, threeCards, highCardList = False, -1, [], []
        same2Ones = self.sameValues(2)
        same3Ones = self.sameValues(3)
        if len(same3Ones[0]) == 1 and len(same2Ones[0]) == 0:
            three, threeValue, threeCards = True, same3Ones[0][0], same3Ones[1]
            for card in self.cards:
                for threeCard in threeCards[0]:
                    if card.value != threeCard.value and card.value not in highCardList:
                        highCardList.append(card.value)
            highCardList.sort(reverse=True)
        return three, threeValue, highCardList, threeCards

    def straight(self):
        straight, straightValue, highCardList = True, -1, []
        values = [card.value for card in self.cards]
        values.sort()
        straightValue = values[4]
        i = 0
        while i < 4:
            if values[i+1] - values[i] != 1:
                straight, straightValue, highCardList = False, -1, values
                break
            i += 1
        return straight, straightValue, highCardList

    def flush(self):
        flush, flushColor, highCardList = False, '', []
        sameness = self.sameColors(5)
        flush = True if sameness[0] != [] else False
        flushColor = Card.colors[sameness[0][0]] if flush == True else ''
        highCardList = [card.value for card in self.cards]
        highCardList.sort()
        return flush, flushColor, highCardList

    def fullHouse(self):
        fullHouse, fullHouseValue, highCardList = False, -1, []
        same2Ones = self.sameValues(2)
        same3Ones = self.sameValues(3)
        if len(same2Ones[0]) == 1 and len(same3Ones[0]) == 1:
            if same2Ones[0][0] != same3Ones[0][0]:
                fullHouse = True
                fullHouseValue = same3Ones[0][0]
                highCardList = [same2Ones[0][0]]
        return fullHouse, fullHouseValue, highCardList

    def four(self):
        four, fourValue, highCardValue = False, -1, -1
        sameness = self.sameValues(4)
        if sameness[0] != []:
            four = True
            fourValue = sameness[0][0]
            for card in self.cards:
                if card.value != fourValue:
                    highCardValue = [card.value]
        return four, fourValue, highCardValue

    def straightFlush(self):
        straightFlush, highCard, highCardList = False, -1, []
        if self.straight()[0] == True and self.flush()[0] == True:
            straightFlush = True
            highCardList = self.highCard()[2]
            highCard = highCardList[0]
        return straightFlush, highCard, highCardList

    def five(self):
        five = False
        sameness = self.sameValues(5)
        if sameness[0] == 5:
            five = True
        return five, self.highCard()[1], self.highCard()[2]

class Game(object):
    def __init__(self, hands = []):
        if hands == []:
            self.deck = Deck()
        else:
            self.handA = hands[0]
            self.handB = hands[1]

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
        
        self.winner = 'draw'
        if self.rankA['rank'] == self.rankB['rank']:
            if self.rankA['value'] == self.rankB['value']:
                i = 0
                while i < len(self.rankA['highCard']): #while i < 4
                    if self.rankA['highCard'][i] > self.rankB['highCard'][i]:
                        self.winner = 'A'
                        break
                    elif self.rankA['highCard'][i] < self.rankB['highCard'][i]:
                        self.winner = 'B'
                        break
                    else:
                        i += 1
            else:
                self.winner = 'A' if self.rankA['value'] > self.rankB['value'] else ('B' if self.rankA['value'] < self.rankB['value'] else 'draw')
        else:
            self.winner = 'A' if self.rankA['rank'] > self.rankB['rank'] else ('B' if self.rankA['rank'] < self.rankB['rank'] else 'draw')


winners = {'A' : 0, 'B' : 0, 'draw' : 0}
n = 100000
start = time.time()
for i in range(n):
    game = Game()
    game.deal()
    game.play()
##    print('--------')
##    game.print()
##    print(game.winner)
    if game.winner == 'draw':
        print('--------')
        game.print()
    winners[game.winner] += 1
print(winners)
end = time.time()
deltaSum = end - start
delta = deltaSum / n
print(delta)

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
##hand = Hand([Card('káró', 2), Card('káró', 3), Card('káró', 4), Card('káró', 5), Card('káró', 6)]) #straightFlush
##hand = Hand([Card('kőr', 2), Card('káró', 2), Card('treff', 2), Card('káró', 4), Card('kőr', 2)]) #five
##hand.print()
##print('1 of the same colors', hand.sameColors(1))
##print('2 of the same colors', hand.sameColors(2))
##print('5 of the same colors', hand.sameColors(5))
##print('1 of the same values', hand.sameValues(1))
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
##print('Four?', hand.four())
##print('Straight flush?', hand.straightFlush())
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
##handA = Hand([Card('treff', 5), Card('kőr', 2), Card('káró', 3), Card('kőr', 'A'), Card('treff', 3)])
##handB = Hand([Card('treff', 9), Card('pikk', 10), Card('kőr', 3), Card('treff', 'J'), Card('pikk', 3)])
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
##    #print(method)
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
