import matplotlib.pyplot as plt
simhei = {
    'family': 'SimHei',
    'weight': 'normal',
    'size': 12,
}

scale = list(range(2, 28, 2))
raw = [0 for _ in range(13)]
with open('contest.result.dat') as f:
    l = [line.strip().split() for line in f]
for index, (winner, score) in enumerate(l):
    bucket = (index // 10) % 13
    if winner == '神算子':
        raw[bucket] += int(score)
    else:
        raw[bucket] -= int(score)
data = [x / 10 for x in raw]
# plt.plot(scale, data, color='blue', marker='.')
# plt.xlim((0, 28))
# plt.ylim((0, 14))
# plt.xticks(scale)
# plt.xlabel('初始纸牌数量', simhei)
# plt.ylabel('「神算子」平均净胜分数', simhei)
# plt.show()
s1 = [int(score) if winner == '神算子' else -int(score) for winner, score in l[:130]]
s2 = [int(score) if winner == '神算子' else -int(score) for winner, score in l[130:]]
s = [s1[i] + s2[i] for i in range(130)]
# k = sorted(enumerate(s), key=lambda x:x[1], reverse=True)
plt.hist(s, bins=54, range=(-19.5, 34.5), color='blue')
plt.xlabel('「神算子」净胜分数', simhei)
plt.ylabel('牌局数量', simhei)
plt.xlim((-10, 40))
plt.ylim((0, 40))
plt.show()