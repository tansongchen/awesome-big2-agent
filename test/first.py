import random
import sys
sys.path.append('..')
from src.awesome import Player
from time import time

POKER = [name for _ in range(4) for name in Player._Player__NAMES]

p = Player()
with open('first.dat', 'a+') as f:
    for firstDepth in range(4, 9):
        p._Player__FIRST_DEPTH = firstDepth
        for _ in range(100):
            poker = POKER[:]
            random.shuffle(poker)
            hand1 = poker[:26]
            hand2 = poker[26:]
            p.newGame(hand1, hand2, 'Opponent')
            start = time()
            p.play([])
            end = time()
            f.write('%d\t%.2f\n' % (firstDepth, end - start))
