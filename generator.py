import random
from awesome import Player
from time import time

POKER = [name for _ in range(4) for name in Player.NAMES]

# 生成 6 + 6 到 12 + 12 的牌局各 100 个，测试性能

p = Player()
with open('test.dat', 'w') as f:
    for scale in range(6, 12):
        for _ in range(1000):
            hand1 = random.choices(POKER, k=scale)
            hand2 = random.choices(POKER, k=scale)
            p.newGame(hand1, hand2, 'Opponent')
            start = time()
            p.play([])
            end = time()
            f.write(' '.join(hand1) + '\n')
            f.write(' '.join(hand2) + '\n')
            f.write(str(end - start) + '\n')