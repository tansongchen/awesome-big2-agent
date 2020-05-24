import random
from awesome import Player
from time import time

POKER = [name for _ in range(4) for name in Player._Player__NAMES]

# # 生成 6 + 6 到 12 + 12 的牌局各 100 个，测试性能

# p = Player()
# with open('test.dat', 'w') as f:
#     for scale in range(4, 10):
#         for _ in range(1):
#             hand1 = random.choices(POKER, k=scale)
#             hand2 = random.choices(POKER, k=scale)
#             p.newGame(hand1, hand2, 'Opponent')
#             start = time()
#             p.play([])
#             end = time()
#             f.write(' '.join(hand1) + '\n')
#             f.write(' '.join(hand2) + '\n')
#             f.write(str(end - start) + '\n')

# 生成 2 + 2 到 26 + 26 的牌局各 100 个

with open('games.dat', 'w') as f:
    for scale in range(2, 28, 2):
        for _ in range(100):
            hand = random.choices(POKER, k=scale * 2)
            hand1 = hand[:scale]
            hand2 = hand[scale:]
            f.write(' '.join(hand1) + '\t' + ' '.join(hand2) + '\n')