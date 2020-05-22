from time import time
from itertools import combinations

class Player:
    NAMES = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    MIN_UTILITY = -100
    MAX_UTILITY = 100
    TIME_LIMIT = 30
    CHECK_TIMEOUT_EVERY = 100000

    def __init__(self):
        self.opponent = None
        self.myList = None
        self.opponentList = None
        self.cache = None
        self.visitedNodes = None
        self.start = None
        self.end = None
        self.maxDepth = None

    def teamName(self) -> str:
        return '神算子'

    def ack(self, t):
        for name in t:
            self.myList.remove(name)
    
    def newGame(self, hand1: list, hand2: list, opponent: str):
        self.opponent = opponent
        self.myList = hand1[:]
        self.opponentList = hand2[:]

    def play(self, t):
        self.start = time()
        for name in t:
            self.opponentList.remove(name)
        myHand = [self.myList.count(name) for name in self.NAMES]
        opponentHand = [self.opponentList.count(name) for name in self.NAMES]
        if t:
            pseudoHand = [t.count(name) for name in self.NAMES]
            _, lastAction = self.branch(pseudoHand, None, smart=True)
        else:
            lastAction = tuple()
        try:
            for maxDepth in range(100, 102):
                self.cache = {}
                self.visitedNodes = 0
                self.maxDepth = maxDepth
                newHand = self.evaluate(myHand, opponentHand, lastAction, self.MIN_UTILITY, self.MAX_UTILITY, 0)
        except TimeoutError:
            pass
        return [self.NAMES[i] for i in self.VALUES for _ in range(myHand[i] - newHand[i])]

    def branch(self, hand, lastAction, smart=False):
        returnList = []
        if lastAction:
            lastTail, length, size, affiliationSize = lastAction
            # 同牌型管牌
            count = 0 if hand[12] < size else 1 if hand[11] < size else 2
            for tail in range(lastTail, 13):
                if hand[tail] >= size:
                    count += 1
                    if count >= length:
                        intermediateHand = hand[:]
                        for index in range(tail, tail - length, -1): intermediateHand[index] -= size
                        if affiliationSize:
                            canAffiliate = [index for index in self.VALUES if hand[index] >= affiliationSize and (index > tail or index <= tail - length)]
                            for combination in combinations(canAffiliate, r=length):
                                newHand = intermediateHand[:]
                                for index in combination: newHand[index] -= affiliationSize
                                returnList.append((newHand, (tail, length, size, affiliationSize)))
                        else:
                            returnList.append((intermediateHand, (tail, length, size, affiliationSize)))
                else:
                    count = 0
            # 炸
            if size != 4:
                for tail in range(13):
                    if hand[tail] == 4:
                        action = (tail, 1, 4, 0)
                        newHand = hand[:]
                        newHand[tail] = 0
                        returnList.append((newHand, action))
            # 过
            returnList.append((hand, tuple()))
        else:
            countList = [0 if hand[12] < i else 1 if hand[11] < i else 2 for i in (1, 2, 3)]
            for tail in self.VALUES:
                if hand[tail] >= 1:
                    countList[0] += 1
                    for length in list(range(countList[0], 4, -1)) + [1]:
                        newHand = hand[:]
                        for index in range(tail, tail - length, -1): newHand[index] -= 1
                        returnList.append((newHand, (tail, length, 1, 0)))
                    if hand[tail] >= 2:
                        countList[1] += 1
                        for length in range(countList[1], 0, -1):
                            newHand = hand[:]
                            for index in range(tail, tail - length, -1): newHand[index] -= 2
                            returnList.append((newHand, (tail, length, 2, 0)))
                        if hand[tail] >= 3:
                            countList[2] += 1
                            for length in range(countList[2], 0, -1):
                                intermediateHand = hand[:]
                                for index in range(tail, tail - length, -1): intermediateHand[index] -= 3
                                returnList.append((intermediateHand, (tail, length, 3, 0)))
                                for affiliationSize in (1, 2):
                                    canAffiliate = [index for index in self.VALUES if hand[index] >= affiliationSize and (index > tail or index <= tail - length)]
                                    for combination in combinations(canAffiliate, r=length):
                                        newHand = intermediateHand[:]
                                        for index in combination: newHand[index] -= affiliationSize
                                        returnList.append((newHand, (tail, length, 3, affiliationSize)))
                        else:
                            countList[2] = 0
                    else:
                        countList[1] = 0
                else:
                    countList[0] = 0
            returnList = sorted(returnList, key=lambda x:(-x[1][1]*(x[1][2]+x[1][3]),x[1][0]))
            # 空炸
            for tail in range(13):
                if hand[tail] == 4:
                    action = (tail, 1, 4, 0)
                    newHand = hand[:]
                    newHand[tail] = 0
                    returnList.append((newHand, action))
        if smart:
            return returnList[0]
        else:
            return returnList

    def evaluate(self, myHand, opponentHand, lastAction, alpha, beta, depth):
        if depth == self.maxDepth:
            newHand, action = self.branch(myHand, lastAction, smart=True)
            if not any(newHand): return sum(opponentHand)
            return -self.evaluate(opponentHand, newHand, action, alpha, beta, depth)
        bestNewHand = []
        key = tuple(myHand) + tuple(opponentHand) + lastAction
        utility = self.cache.get(key)
        if utility is not None: return utility
        self.visitedNodes += 1
        if self.visitedNodes % self.CHECK_TIMEOUT_EVERY == 0:
            self.end = time.time()
            if self.end - self.start > self.TIME_LIMIT - 1: raise TimeoutError()
        utility = self.MIN_UTILITY
        for newHand, action in self.branch(myHand, lastAction):
            if not any(newHand):
                utility = sum(opponentHand)
                if depth == 0: bestNewHand = newHand
                break
            newUtility = -self.evaluate(opponentHand, newHand, action, -beta, -alpha, depth + 1)
            if newUtility >= utility:
                utility = newUtility
                alpha = max(alpha, utility)
                if depth == 0: bestNewHand = newHand
                if utility >= beta: break
        self.cache[key] = utility
        if depth == 0:
            return bestNewHand
        else:
            return utility
