import random
import sys
sys.path.append('..')
from src.awesome import Player

POKER = [name for _ in range(4) for name in Player._Player__NAMES]

with open('games.dat', 'w') as f:
    for scale in range(2, 28, 2):
        for _ in range(100):
            hand = random.choices(POKER, k=scale * 2)
            hand1 = hand[:scale]
            hand2 = hand[scale:]
            f.write(' '.join(hand1) + '\t' + ' '.join(hand2) + '\n')