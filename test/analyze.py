import matplotlib.pyplot as plt
import matplotlib.font_manager
PingFang = matplotlib.font_manager.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
with open('test.dat') as f:
    fl = f.readlines()

font1 = {'family' : 'SimHei',
'weight' : 'normal',
'size'   : 12,
}
l = []
time = []
for i in range(len(fl) // 3):
    l.append((
        tuple(fl[3*i].strip().split()),
        tuple(fl[3*i+1].strip().split())
        ))
    time.append(float(fl[3*i+2].strip()))

# Feature：长度

cardLenFeature = lambda x: len(x[0])
cardLevelFeature = lambda x: (len(set(x[0])) + len(set(x[1])))
cardLen = list(map(cardLenFeature, l))
cardLevel = list(map(cardLevelFeature, l))
plt.semilogy(cardLen, time, '.', color='blue')
plt.xlim((5, 12))
plt.ylim((1e-4, 1e2))
plt.xlabel('纸牌数量', font1)
plt.ylabel('精确解用时（秒）', font1)
# plt.semilogy(cardLevel, time, '.', color="blue", Marker='.')
plt.show()