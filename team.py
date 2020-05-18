from helper import Action, CARDS, findAllActions
from copy import copy
import random
import time

class Player:
    MAX_UTILITY = 100
    MIN_UTILITY = -100
    TIME_LIMIT = 30
    CHECK_TIMEOUT_EVERY = 10000

    def __init__(self):
        self.opponent = None
        self.myList = None
        self.opponentList = None
        self.cache = None
        self.MAX_DEPTH = None
        self.visitedNodes = None
        self.start = None
        self.end = None

    def teamName(self) -> str:
        return 'Awesome Big2 Agent'
    
    def newGame(self, hand1: list, hand2: list, opponent: str):
        self.opponent = opponent
        self.myList = copy(hand1)
        self.opponentList = copy(hand2)

    def hash(self, cnd):
        return tuple(cnd[card] for card in CARDS)

    def play(self, turn: list) -> list:
        self.start = time.time()
        for name in turn:
            self.opponentList.remove(name)
        myCND = {card: self.myList.count(card.name) for card in CARDS}
        opponentCND = {card: self.opponentList.count(card.name) for card in CARDS}
        actionList = findAllActions(myCND)
        opponentAction = self.interpret(turn)
        biggerActionList = [myAction for myAction in actionList if myAction > opponentAction]
        try:
            for depth in range(5, 20):
                self.MAX_DEPTH = depth
                self.visitedNodes = 0
                self.cache = {}
                select = lambda action: self.minimize(self.respond(myCND, action), opponentCND, action, alpha=self.MIN_UTILITY, beta=self.MAX_UTILITY, depth=1)
                bestAction = max(biggerActionList, key=select)
            return bestAction.show()
        except TimeoutError:
            return bestAction.show()

    def ack(self, actualTurn):
        for name in actualTurn:
            self.myList.remove(name)

    def interpret(self, turn: list):
        cardNumberDict = {card: turn.count(card.name) for card in CARDS}
        allActions = findAllActions(cardNumberDict)
        return [action for action in allActions if action.getTotalNumber() == len(turn)][0]

    def respond(self, cnd: dict, action: Action):
        newCND = copy(cnd)
        for card in action.chain:
            newCND[card] -= action.size
        for affiliation in action.affiliationList:
            newCND[affiliation] -= action.affiliationSize
        return newCND

    def maximize(self, oneCND: dict, anotherCND: dict, lastAction: Action, alpha, beta, depth):
        self.visitedNodes += 1
        if self.visitedNodes % self.CHECK_TIMEOUT_EVERY == 0:
            self.end = time.time()
            if self.end - self.start > self.TIME_LIMIT - 1:
                raise TimeoutError()
        key = self.hash(oneCND) + self.hash(anotherCND) + lastAction.hash()
        if key in self.cache:
            return self.cache[key]
        if not any(oneCND.values()): return sum(anotherCND.values())
        if not any(anotherCND.values()): return -sum(oneCND.values())
        if depth == self.MAX_DEPTH: return self.evaluate(oneCND, anotherCND, lastAction, True)
        actionList = sorted([action for action in findAllActions(oneCND) if action > lastAction], key=lambda x: x.getTotalNumber(), reverse=True)
        value = self.MIN_UTILITY
        for action in actionList:
            value = max(value, self.minimize(self.respond(oneCND, action), anotherCND, action, alpha, beta, depth + 1))
            if value >= beta: return value
            alpha = max(alpha, value)
        self.cache[key] = value
        return value

    def minimize(self, oneCND: dict, anotherCND: dict, lastAction: Action, alpha, beta, depth):
        self.visitedNodes += 1
        if self.visitedNodes % self.CHECK_TIMEOUT_EVERY == 0:
            self.end = time.time()
            if self.end - self.start > self.TIME_LIMIT - 1:
                raise TimeoutError()
        key = self.hash(oneCND) + self.hash(anotherCND) + lastAction.hash()
        if key in self.cache:
            return self.cache[key]
        if not any(oneCND.values()): return sum(anotherCND.values())
        if not any(anotherCND.values()): return -sum(oneCND.values())
        if depth == self.MAX_DEPTH: return self.evaluate(oneCND, anotherCND, lastAction, False)
        actionList = sorted([action for action in findAllActions(anotherCND) if action > lastAction], key=lambda x: x.getTotalNumber(), reverse=True)
        value = self.MAX_UTILITY
        for action in actionList:
            value = min(value, self.maximize(oneCND, self.respond(anotherCND, action), action, alpha, beta, depth + 1))
            if value <= alpha: return value
            beta = min(beta, value)
        self.cache[key] = value
        return value
    
    def evaluate(self, oneCND: dict, anotherCND: dict, lastAction: Action, isMyTurn: bool):
        if not any(oneCND.values()): return sum(anotherCND.values())
        if not any(anotherCND.values()): return -sum(oneCND.values())
        if isMyTurn:
            actionList = sorted([action for action in findAllActions(oneCND) if action > lastAction], key=lambda x: x.getTotalNumber(), reverse=True)
            bestAction = actionList[0]
            forwardCND = self.respond(oneCND, bestAction)
            return self.evaluate(forwardCND, anotherCND, bestAction, not isMyTurn)
        else:
            actionList = sorted([action for action in findAllActions(anotherCND) if action > lastAction], key=lambda x: x.getTotalNumber(), reverse=True)
            bestAction = actionList[0]
            forwardCND = self.respond(anotherCND, bestAction)
            return self.evaluate(oneCND, forwardCND, bestAction, not isMyTurn)