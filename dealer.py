import copy
import collections

class Dealer:
    def __init__(self, v):
        self.version = v
        self.prec = {}
        self.prec['3'] = 1
        self.prec['4'] = 2
        self.prec['5'] = 3
        self.prec['6'] = 4
        self.prec['7'] = 5
        self.prec['8'] = 6
        self.prec['9'] = 7
        self.prec['10'] = 8
        self.prec['J'] = 9
        self.prec['Q'] = 10
        self.prec['K'] = 11
        self.prec['A'] = 12
        self.prec['2'] = 13
        self.games = ((['A', 'A'], ['2', '3', '3']),
                      (['A', 'A', '9'], ['2', 'Q', 'Q','Q', '10', '10', '7', '7', '5', '5', '3']))

    def sublist(self, t):
        sub = collections.Counter(t)
        par = collections.Counter(self.cards[self.curr])
        for k, v in sub.items():
            if v > par.get(k, 0):
                return False
        return True

    def deal(self, num):
        self.curr = 0
        self.t = []
        self.cards = copy.deepcopy(self.games[num])
        return copy.deepcopy(self.cards)

    def check(self, t):
        if self.sublist(t) and self.beat(t, self.t):
            self.t = t
        else:
            self.t = [] if self.t else [self.cards[self.curr][0]]
        for c in self.t:
            self.cards[self.curr].remove(c)

        clear = not self.cards[self.curr]
        self.curr = 1 - self.curr
        score = len(self.cards[self.curr]) if clear else None
        return score, self.t

    def seq(self, s):
        if self.prec[s[-1]] - self.prec[s[0]] + 1 == len(s):
            return (len(s), s[-1])
        elif self.prec[s[-1]] - self.prec[s[0]] == 12:  # loop
            tail = -3 if s[-2] == 'A' else -2
            if self.prec[s[tail]] == len(s) + tail + 1:
                return (len(s), s[tail])
            else:
                return None

    def pattern(self, t):
        if not t:
            return None
        counter = dict((c, t.count(c)) for c in set(t))
        m = max(counter.values())
        if m == 1:  # 单张或顺子
            s = self.seq(sorted(t, key=lambda x: self.prec[x]))
            if not s:
                return None
            if s[0] == 1 or s[0] > 4:
                return ('single*{}'.format(s[0]), s[1])
            else:
                return None
        if m == 2:  # 对子或连对
            for v in counter.values():
                if v != 2:
                    return None
            s = self.seq(sorted(counter.keys(), key=lambda x: self.prec[x]))
            if not s:
                return None
            return ('pair*{}'.format(s[0]), s[1])
        if m == 3:
            s = self.seq(sorted([k for k in counter if counter[k] == 3],
                                key=lambda x: self.prec[x]))
            if not s:
                return None
            aff = [counter[k] for k in counter if counter[k] < 3]
            ptt = ''
            if not aff:
                ptt = 'triple*{}'
            elif aff == [1] * s[0]:
                ptt = 'triple*{}+single'
            elif aff == [2] * s[0]:
                ptt = 'triple*{}+pair'
            else:
                return None
            return (ptt.format(s[0]), s[1])
        if m == 4:
            if len(counter) > 1:  # 没有连炸
                return None
            return ('bomb', t[0])
        return None

    def beat(self, t, yt):
        t = self.pattern(t)
        yt = self.pattern(yt)
        if not t:
            return False
        if not yt:
            return True
        if t[0] == 'bomb' and yt[0] != 'bomb':  # 炸弹盖过其他牌型
            return True
            # 牌型匹配且大于
        return t[0] == yt[0] and self.prec[t[1]] > self.prec[yt[1]]