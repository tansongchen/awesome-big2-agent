import random
from copy import copy
from pythonds import Queue

VALUE = {
    '3': 0,
    '4': 1,
    '5': 2,
    '6': 3,
    '7': 4,
    '8': 5,
    '9': 6,
    '10': 7,
    'J': 8,
    'Q': 9,
    'K': 10,
    'A': 11,
    '2': 12
}

class Card:

    def __init__(self, name):
        self.name = name
        self.value = VALUE[self.name]
    
    def __sub__(self, integer):
        value = self.value - integer
        if value < 0: value = value + 13
        return CARDS[value]
    
    def __gt__(self, another):
        return self.value > another.value

# 由于 Card 是一个 Soliton 类，所以必须事先把需要的卡片做成引用
CARDS = [Card(name) for name in VALUE.keys()]
MAX_CARD_IN_HAND = 26
SINGLE_MIN_CHAIN_LENGTH = 5

class Action:
    size = 0
    affiliationSize = 0

    def __init__(self, tail, length, affiliationList=[]):
        self.tail = tail
        self.length = length
        self.affiliationList = affiliationList
        self.chain = [self.tail - i for i in range(self.length)]

    def hash(self):
        return (self.tail.value, self.size, self.length)

    def getTotalNumber(self):
        return (self.size + self.affiliationSize) * self.length

    def show(self):
        return [card.name for card in self.chain for _ in range(self.size)] + [card.name for card in self.affiliationList for _ in range(self.affiliationSize)]

    def __gt__(self, another):
        return isinstance(another, Pass) or (isinstance(another, type(self)) and self.length == another.length and self.tail > another.tail)

    def augment(self, cardNumberDict: dict):
        # 增长得到顺子
        augmentedActionList = []
        if isinstance(self, Single) and self.length == 1:
            nextCards = [(self.tail - i) for i in range(1, SINGLE_MIN_CHAIN_LENGTH)]
        else:
            nextCards = [self.tail - self.length]
        if all(cardNumberDict[card] >= self.size and card not in self.chain for card in nextCards):
            action = type(self)(self.tail, self.length + len(nextCards))
            augmentedActionList.append(action)
        return augmentedActionList

class Pass(Action):
    def __init__(self):
        self.tail = 0
        self.length = 0
        self.chain = []
        self.affiliationList = []

    def __gt__(self, another):
        return not isinstance(another, Pass)

    def hash(self):
        return (self.tail, self.size, self.length)

class Single(Action):
    size = 1

class Double(Action):
    size = 2

class Triple(Action):
    size = 3

class AffiliatingAction(Action):
    size = 3

    def augment(self, cardNumberDict):
        augmentedList = []
        nextCard = self.tail - self.length
        if nextCard not in self.affiliationList and cardNumberDict[nextCard] >= self.size:
            tempDict = {k: v for k, v in cardNumberDict.items() if k not in self.chain and k != nextCard}
            for affiliation in self.affiliationList:
                tempDict[affiliation] -= self.affiliationSize
            for affiliation, number in tempDict.items():
                if number >= self.affiliationSize:
                    newAffiliationList = copy(self.affiliationList)
                    newAffiliationList.append(affiliation)
                    action = type(self)(self.tail, self.length + 1, newAffiliationList)
                    augmentedList.append(action)
        return augmentedList

class TripleWithOne(AffiliatingAction):
    affiliationSize = 1

class TripleWithTwo(AffiliatingAction):
    affiliationSize = 2

class Quadruple(Action):
    size = 4

    def augment(self, cardNumberDict):
        return []
    
    def __gt__(self, another):
        return not isinstance(another, Quadruple) or self.tail > another.tail

def findAllActions(cardNumberDict):
    actionList = [Pass()]
    queue = Queue()
    # 这块不优雅，但速度快，所以就先这么写了
    for card, number in cardNumberDict.items():
        if number >= 1:
            queue.enqueue(Single(card, 1))
            if number >= 2:
                queue.enqueue(Double(card, 1))
                if number >= 3:
                    queue.enqueue(Triple(card, 1))
                    for affiliatedCard, affiliatedNumber in cardNumberDict.items():
                        if affiliatedCard != card:
                            if affiliatedNumber >= 1:
                                queue.enqueue(TripleWithOne(card, 1, [affiliatedCard]))
                                if affiliatedNumber >= 2:
                                    queue.enqueue(TripleWithTwo(card, 1, [affiliatedCard]))
                    if number == 4:
                        queue.enqueue(Quadruple(card, 1))
    while not queue.isEmpty():
        action = queue.dequeue()
        actionList.append(action)
        augmentedActionList = action.augment(cardNumberDict)
        for item in augmentedActionList:
            queue.enqueue(item)
    return actionList

if __name__ == '__main__':
    from timeit import Timer
    from random import choices
    allNames = [card.name for card in CARDS for _ in range(4)]
    totalTime = 0
    for _ in range(100):
        hand = choices(allNames, k=26)
        cardNumberDict = {card: hand.count(card.name) for card in CARDS}
        t = Timer('actionList = findAllActions(cardNumberDict)', 'from __main__ import cardNumberDict, findAllActions')
        totalTime += t.timeit(10)
    print(totalTime / 1000)
    # for action in actionList:
    #     print(action.show())