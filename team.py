from helper import Card, CARDS, findAllActions
from copy import copy
import random

class Player:
    def __init__(self):
        self.agent = RandomAgent()
        self.opponent = None
        self.myList = None
        self.opponentList = None

    def teamName(self) -> str:
        return self.agent.name
    
    def newGame(self, hand1:list, hand2:list, opponent:str):
        self.opponent = opponent
        self.myList = copy(hand1)
        self.opponentList = copy(hand2)

    def play(self, turn:list) -> list:
        if turn:
            for name in turn:
                self.opponentList.remove(name)
            nextTurn = self.agent.desideToDefend(self.myList, self.opponentList, turn)
        else:
            nextTurn = self.agent.desideToInitiate(self.myList, self.opponentList)
        return nextTurn

    def ack(self, actualTurn):
        for name in actualTurn:
            self.myList.remove(name)

class Agent:

    def findAllActionsForCurrentHand(self, hand: list):
        cardNumberDict = {card: hand.count(card.name) for card in CARDS}
        return findAllActions(cardNumberDict)

    def interpret(self, turn: list):
        cardNumberDict = {card: turn.count(card.name) for card in CARDS}
        allActions = findAllActions(cardNumberDict)
        return [action for action in allActions if action.getTotalNumber() == len(turn)][0]

    def desideToInitiate(self, myList, opponentList):
        raise NotImplementedError("Agent 类必须重写决策方法")

    def desideToDefend(self, myList, opponentList, turn):
        raise NotImplementedError("Agent 类必须重写决策方法")

class RandomAgent(Agent):
    """
    在所有可能的出牌行为中随机选取一个
    """
    def __init__(self):
        self.name = '随机的玩家'

    def desideToInitiate(self, myList, opponentList):
        actionList = self.findAllActionsForCurrentHand(myList)
        action = random.choice(actionList)
        return action.show()

    def desideToDefend(self, myList, opponentCardList, turn):
        actionList = self.findAllActionsForCurrentHand(myList)
        opponentAction = self.interpret(turn)
        biggerActionList = [myAction for myAction in actionList if myAction > opponentAction]
        if biggerActionList:
            biggerAction = random.choice(biggerActionList)
            return biggerAction.show()
        else:
            return []

class SmartAgent(Agent):
    """
    出小牌，类似于托管
    """
    def __init__(self):
        self.name = '聪明的玩家'

    def desideToInitiate(self, myList, opponentList):
        actionList = self.findAllActionsForCurrentHand(myList)
        action = actionList[0]
        return action.show()

    def desideToDefend(self, myCardList, opponentCardList, turn):
        actionList = self.findAllActionsForCurrentHand(myList)
        opponentAction = self.interpret(turn)
        biggerActionList = [myAction for myAction in actionList if myAction > opponentAction]
        if biggerActionList:
            biggerAction = biggerActionList[0]
            return biggerAction.show()
        else:
            return []

class AwesomeAgent(Agent):
    """
    我们最后提交上去的版本
    """

    def __init__(self):
        self.name = 'Awesome Big2 Agent'
