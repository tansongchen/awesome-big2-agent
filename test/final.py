data = []
with open('final.dat') as f:
    for line in f:
        t1, t2, score_s, game = line.strip().split('\t')
        data.append((t1, t2, int(score_s), int(game) - 1))

tl = [x[0] for x in data]
totalScore = {k: 0 for k in set(tl)}
totalGame = {k: 0 for k in set(tl)}
dev = {k: [0 for _ in range(10)] for k in set(tl)}

for t1, t2, score, game in data:
    totalScore[t1] += score
    totalScore[t2] -= score
    v = 1 if score > 0 else -1
    totalGame[t1] += v
    totalGame[t2] -= v
    dev[t1][game] += score
    dev[t2][game] -= score

sortts = sorted(totalScore.items(), key=lambda x:x[1], reverse=True)
r = lambda x, l: sum(1 if x < item else 0 for item in l)

rank = {k: [r(dev[k][i], [v[i] for x, v in dev.items()]) for i in range(10)]
    for k in dev}

avg = lambda l: sum(l) / len(l)
dev = lambda l: (sum([x**2 for x in l]) / len(l) - avg(l)**2)**0.5
rankdev = {k: dev(v) for k, v in rank.items()}
with open('report.dat', 'w') as f:
    f.write('%s\t%s\t%s\t%s\n' % ('队名', '净胜分数', '净胜局数', '局间波动'))
    for t, score in sortts:
        f.write('%s\t%d\t%d\t%.2f\n' % (t, score, totalGame[t], rankdev[t]))