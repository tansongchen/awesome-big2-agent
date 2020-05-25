import random
import sys
sys.path.append('..')
from src.awesome import Player

POKER = [name for _ in range(4) for name in Player._Player__NAMES]
values ={'3':0 ,'4':1 ,'5':2 ,'6':3 ,'7':4 ,'8':5 ,'9':6 ,'10':7 ,'J':8 ,'Q':9 ,'K':10 ,'A':11 ,'2':12 }

with open('benchmark.games.dat', 'w') as f:
    for scale in range(2, 28, 2):
        for _ in range(10):
            poker = POKER[:]
            random.shuffle(poker)
            hand1 = sorted(poker[0:scale], key=lambda x: values[x])
            hand2 = sorted(poker[scale:2*scale], key=lambda x: values[x])
            f.write(' '.join(hand1) + '\t' + ' '.join(hand2) + '\n')