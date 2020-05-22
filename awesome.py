from time import time
from itertools import combinations

class Player:
    # 由所有纸牌名称顺序构成的列表
    NAMES = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    # 由所有纸牌指标顺序构成的列表
    VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # 最小效用值
    MIN_UTILITY = -100
    # 最大效用值
    MAX_UTILITY = 100
    # 搜索时限
    TIME_LIMIT = 30
    # 每访问该数量的节点就检查是否超时
    CHECK_TIMEOUT_EVERY = 100000

    def __init__(self):
        # 对方名称
        self.opponent = None
        # 己方所有纸牌名称构成的列表
        self.myList = None
        # 对方所有纸牌名称构成的列表
        self.opponentList = None
        # 在搜索中暂存中间节点值的字典
        self.cache = None
        # 统计已经访问节点的个数
        self.visitedNodes = None
        # 搜索开始时间
        self.start = None
        # 搜索结束时间
        self.end = None
        # 搜索最大深度
        self.maxDepth = None

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
        self.opponent = opponent
        self.myList = hand1[:]
        self.opponentList = hand2[:]

    def play(self, t):
        """
        给定对方的牌型，返回己方反馈的牌型\n
        t: 对方牌型中纸牌名称列表
        """
        self.start = time()
        for name in t:
            self.opponentList.remove(name)
        myHand = [self.myList.count(name) for name in self.NAMES]
        opponentHand = [self.opponentList.count(name) for name in self.NAMES]
        # 由于分枝函数在 smart 模式下总是返回最长的行动，因此这一方法可以把对方的牌型解析为牌型四元组
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

    def ack(self, t):
        """
        裁判裁定结果后，将实际能出的纸牌名称列表传回用于更新状态
        t: 裁定后的纸牌名称列表
        """
        for name in t:
            self.myList.remove(name)

    def branch(self, hand, lastAction, smart=False):
        """
        给定手牌列表和上一轮牌型，求所有可能行动
        hand: 手牌列表\n
        lastAction: 上一轮牌型四元组\n
        smart: 是否启用「智多星」模式\n
        """
        returnList = []
        if lastAction:
            lastTail, length, size, affiliationSize = lastAction
            # 同一类牌型的可能行动
            count = 0 if hand[12] < size else 1 if hand[11] < size else 2
            for tail in self.VALUES:
                if hand[tail] >= size:
                    count += 1
                    if tail > lastTail and count >= length:
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
            # 炸弹
            if size != 4:
                for tail in range(13):
                    if hand[tail] == 4:
                        action = (tail, 1, 4, 0)
                        newHand = hand[:]
                        newHand[tail] = 0
                        returnList.append((newHand, action))
            # 不出
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
        """
        递归地对节点的极小极大值进行求值，返回最优选择对应的剩余手牌列表\n
        myHand: 节点处己方手牌列表\n
        opponentHand: 节点处对方手牌列表\n
        lastAction: 对方上一轮的行动\n
        alpha: 在该条路径上，己方效用的极大值
        beta: 在该条路径上，对方能使己方效用达到的最小值
        depth: 当前节点的深度
        """
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
