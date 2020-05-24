import matplotlib.pyplot as plt
simhei = {
    'family': 'SimHei',
    'weight': 'normal',
    'size': 12,
}

scale = list(range(2, 28, 2))
raw = [0 for _ in range(13)]
with open('benchmark.result.dat') as f:
    l = [line.strip().split() for line in f]
for index, (winner, score) in enumerate(l):
    bucket = (index // 100) % 13
    if winner == '智多星':
        raw[bucket] -= int(score)
    else:
        raw[bucket] += int(score)
data = [x / 1300 for x in raw]
plt.plot(scale, data, color='blue', marker='.')
plt.xlim((0, 28))
plt.ylim((-8, 8))
plt.xticks(scale)
plt.xlabel('初始纸牌数量', simhei)
plt.ylabel('「神算子」平均净胜分数', simhei)
plt.show()