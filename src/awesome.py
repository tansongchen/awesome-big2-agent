from time import time
from itertools import combinations

class Player:
    # 由所有纸牌名称顺序构成的列表
    __NAMES = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    # 由所有纸牌指标顺序构成的列表
    __VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # 最小效用值
    __MIN_UTILITY = -100
    # 最大效用值
    __MAX_UTILITY = 100
    # 搜索时限
    __TIME_LIMIT = 30
    # 每访问该数量的节点就检查是否超时
    __CHECK_TIMEOUT_EVERY = 1000
    # 开始求近似解的规模阈值
    __ESTIMATION_THRESHOLD = 10
    # 初次搜索深度
    __FIRST_DEPTH = 8
    # 最大搜索深度
    __MAX_DEPTH = 100

    def __init__(self):
        # 对方名称
        self.__opponent = None
        # 己方所有纸牌名称构成的列表
        self.__myList = None
        # 对方所有纸牌名称构成的列表
        self.__opponentList = None
        # 在搜索中暂存中间节点值的字典
        self.__cache = None
        # 统计已经访问节点的个数
        self.__visitedNodes = None
        # 搜索开始时间
        self.__start = None
        # 搜索结束时间
        self.__end = None
        # 搜索最大深度
        self.__maxDepth = None

    def teamName(self):
        """
        智能体名称
        """
        return '神算子'

    def newGame(self, hand1, hand2, opponent):
        """
        初始化对方名称，己方和对方的纸牌名称列表\n
        hand1: 己方的纸牌名称列表\n
        hand2: 对方的纸牌名称列表\n
        opponent: 对方名称
        """
        self.__opponent = opponent
        self.__myList = hand1[:]
        self.__opponentList = hand2[:]
        self.__cache = None
        self.__start = None
        self.__end = None
        self.__maxDepth = None

    def play(self, t):
        """
        给定对方的牌型，返回己方反馈的牌型\n
        t: 对方牌型中纸牌名称列表
        """
        self.__start = time()
        for name in t:
            self.__opponentList.remove(name)
        myHand = [self.__myList.count(name) for name in self.__NAMES]
        opponentHand = [self.__opponentList.count(name) for name in self.__NAMES]
        # 找出分枝函数所能返回最长的行动，从而把对方的牌型解析为牌型四元组
        if t:
            pseudoHand = [t.count(name) for name in self.__NAMES]
            _, lastAction = sorted(self.__branch(pseudoHand, None), key=lambda x:x[1][1]*(x[1][2]+x[1][3]), reverse=True)[0]
        else:
            lastAction = tuple()
        newHand, action = self.__branch(myHand, lastAction, smart=True)
        if max(len(self.__myList), len(self.__opponentList)) <= self.__ESTIMATION_THRESHOLD:
            self.__cache = {}
            self.__visitedNodes = 0
            self.__maxDepth = self.__MAX_DEPTH
            newHand = self.__evaluate(myHand, opponentHand, lastAction, self.__MIN_UTILITY, self.__MAX_UTILITY, 0)
        else:
            try:
                for maxDepth in range(self.__FIRST_DEPTH, self.__MAX_DEPTH):
                    self.__cache = {}
                    self.__visitedNodes = 0
                    self.__maxDepth = self.__FIRST_DEPTH
                    newHand = self.__evaluate(myHand, opponentHand, lastAction, self.__MIN_UTILITY, self.__MAX_UTILITY, 0)
            except TimeoutError:
                pass
        return [self.__NAMES[i] for i in self.__VALUES for _ in range(myHand[i] - newHand[i])]

    def ack(self, t):
        """
        裁判裁定结果后，将实际能出的纸牌名称列表传回用于更新状态
        t: 裁定后的纸牌名称列表
        """
        for name in t:
            self.__myList.remove(name)

    def __branch(self, hand, lastAction, smart=False):
        """
        给定手牌列表和上一轮牌型，求所有可能行动
        hand: 手牌列表\n
        lastAction: 上一轮牌型四元组\n
        smart: 是否启用「智多星」模式\n
        """
        returnList = []
        if lastAction:
            lastTail, length, size, affiliationSize = lastAction
            count = 0 if hand[-1] < size else 1 if hand[-2] < size else 2
            for tail in self.__VALUES:
                if hand[tail] >= size:
                    count = min(count + 1, 13)
                    if tail > lastTail and count >= length:
                        intermediateHand = hand[:]
                        for index in range(tail, tail - length, -1): intermediateHand[index] -= size
                        if affiliationSize:
                            canAffiliate = [index for index in self.__VALUES if hand[index] >= affiliationSize and (index > tail or index <= tail - length)]
                            for combination in combinations(canAffiliate, r=length):
                                newHand = intermediateHand[:]
                                for index in combination: newHand[index] -= affiliationSize
                                returnList.append((newHand, (tail, length, size, affiliationSize)))
                        else:
                            returnList.append((intermediateHand, (tail, length, size, affiliationSize)))
                else:
                    count = 0
            if size != 4:
                for tail in self.__VALUES:
                    if hand[tail] == 4:
                        action = (tail, 1, 4, 0)
                        newHand = hand[:]
                        newHand[tail] = 0
                        returnList.append((newHand, action))
            returnList.append((hand, tuple()))
        else:
            countList = [0 if hand[-1] < size else 1 if hand[-2] < size else 2 for size in (1, 2, 3)]
            for tail in self.__VALUES:
                if hand[tail] >= 1:
                    countList[0] = min(countList[0] + 1, 13)
                    for length in list(range(countList[0], 4, -1)) + [1]:
                        newHand = hand[:]
                        for index in range(tail, tail - length, -1): newHand[index] -= 1
                        returnList.append((newHand, (tail, length, 1, 0)))
                    if hand[tail] >= 2:
                        countList[1] = min(countList[1] + 1, 13)
                        for length in range(countList[1], 0, -1):
                            newHand = hand[:]
                            for index in range(tail, tail - length, -1): newHand[index] -= 2
                            returnList.append((newHand, (tail, length, 2, 0)))
                        if hand[tail] >= 3:
                            countList[2] = min(countList[2] + 1, 13)
                            for length in range(countList[2], 0, -1):
                                intermediateHand = hand[:]
                                for index in range(tail, tail - length, -1): intermediateHand[index] -= 3
                                returnList.append((intermediateHand, (tail, length, 3, 0)))
                                usedIndexes = [x % 13 for x in range(tail, tail - length, -1)]
                                for affiliationSize in (1, 2):
                                    canAffiliate = [index for index in self.__VALUES if hand[index] >= affiliationSize and index not in usedIndexes]
                                    for combination in combinations(canAffiliate, r=length):
                                        newHand = intermediateHand[:]
                                        for index in combination: newHand[index] -= affiliationSize
                                        returnList.append((newHand, (tail, length, 3, affiliationSize)))
                        else:
                            countList[2] = 0
                    else:
                        countList[1] = 0
                        countList[2] = 0
                else:
                    countList[0] = 0
                    countList[1] = 0
                    countList[2] = 0
            returnList.sort(key=lambda x:(-x[1][1]*(x[1][2]+x[1][3]),x[1][0]))
            for tail in self.__VALUES:
                if hand[tail] == 4:
                    action = (tail, 1, 4, 0)
                    newHand = hand[:]
                    newHand[tail] = 0
                    returnList.append((newHand, action))
        if smart:
            return returnList[0]
        else:
            return returnList

    def __evaluate(self, myHand, opponentHand, lastAction, alpha, beta, depth):
        """
        递归地对节点的极小极大值进行求值，返回最优选择对应的剩余手牌列表\n
        myHand: 节点处己方手牌列表\n
        opponentHand: 节点处对方手牌列表\n
        lastAction: 对方上一轮的行动\n
        alpha: 在该条路径上，己方效用的极大值
        beta: 在该条路径上，对方能使己方效用达到的最小值
        depth: 当前节点的深度
        """
        key = tuple(myHand) + tuple(opponentHand) + lastAction
        utility = self.__cache.get(key)
        if utility is not None: return utility
        if depth == self.__maxDepth:
            return sum(opponentHand) - sum(myHand)
        self.__visitedNodes += 1
        if self.__visitedNodes % self.__CHECK_TIMEOUT_EVERY == 0:
            self.__end = time()
            if self.__end - self.__start > self.__TIME_LIMIT - 1: raise TimeoutError()
        utility = self.__MIN_UTILITY
        bestNewHand = []
        for newHand, action in self.__branch(myHand, lastAction):
            if not any(newHand):
                utility = sum(opponentHand)
                if depth == 0: bestNewHand = newHand
                break
            newUtility = -self.__evaluate(opponentHand, newHand, action, -beta, -alpha, depth + 1)
            if newUtility > utility:
                utility = newUtility
                alpha = max(alpha, utility)
                if depth == 0: bestNewHand = newHand
                if alpha >= beta: break
        self.__cache[key] = utility
        if depth == 0:
            return bestNewHand
        else:
            return utility
