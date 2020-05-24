import matplotlib.pyplot as plt
simhei = {
    'family': 'SimHei',
    'weight': 'normal',
    'size': 12,
}

with open('first.dat') as f:
    l = [line.strip().split() for line in f]
firstDepth = [int(x[0]) for x in l]
time = [float(x[1]) for x in l]
plt.semilogy(firstDepth, time, '.', color='blue')
plt.xlim((3, 11))
plt.ylim((1e-4, 1e2))
plt.xlabel('初次搜索深度', simhei)
plt.ylabel('初次搜索用时（秒）', simhei)
plt.show()