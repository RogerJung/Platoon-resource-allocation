import matplotlib.pyplot as plt


x = [50, 70, 90, 110, 130, 150, 170, 190, 200]
# random
y1 = [20.827, 19.919, 15.633, 16.086, 13.969, 14.170, 13.313, 13.111, 13.364]
# DQN
y2 = [26.928, 30.711, 8.018, 14.926, 19.566, 11.346, 1.412, 9.480, 1.512]

plt.plot(x, y1, marker="o", markersize=4, color="orange", label='random')
plt.plot(x, y2, marker="o", markersize=4, color="blue", label='DQN')
plt.ylabel('Packet Collision Probability(%)')
plt.xlabel('Selection Windows Size(RB/s)')
plt.legend(loc=1)

plt.show()
plt.savefig('result.png')