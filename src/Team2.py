class Player:
    def __init__(self):
        self.name = "keyboard:p"
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
        pass
    
    def newGame(self, hand1, hand2, opponent):
        self.myHand = hand1
        self.yourHand = hand2
        self.opponent = opponent

    def play(self, t):
        for c in t:
            self.yourHand.remove(c)
        t = input(self.teamName()+" :==>").split()
        return t

    def ack(self, t):
        #print("ack: {}".format(self.myHand))
        for c in t:
            self.myHand.remove(c)

    def teamName(self):
        return self.name
