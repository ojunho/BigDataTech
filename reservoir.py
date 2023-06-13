import random
import matplotlib.pyplot as plt
import numpy as np

class Reservoir:
    def __init__(self, k):
        self.k = k
        self.sampled = []
        self.size = 0

    def add(self, x):
        self.size += 1
        if self.size <= self.k:
            self.sampled.append(x)
            return 1
        else:
            i = random.randrange(0, self.size)
            if i < self.k:
                self.sampled[i] = x
                return 1
            return 0

#Reservoir with Replacement
class RR:
    def __init__(self, k):
        self.k = k
        self.size = 0
        self.sampled = [[] for _ in range(k)]

    def add(self, x):
        self.size += 1
        if self.size <= 1:
            for i in range(self.k):
                self.sampled[i].append(x)
            return self.k
    
        else:
            tmp = 0
            for i in range(self.k):
                a = random.randrange(0, self.size)
                if a < 1:
                    self.sampled[i][a] = x
                    tmp += 1
            return tmp
                
                
# reservoir
r = Reservoir(100)
countR = [0 for _ in range(1000)]
for i in range(10000):
    for j in range(1000):
        cntR = r.add(j)
        countR[j] += cntR
    print(i, "th attempt complete")

#reservoir with replacement
rr = RR(100)
countRR = [0 for _ in range(1000)]
for i in range(10000):
    for j in range(1000):
        cntRR = rr.add(j)
        countRR[j] += cntRR
    print(i, "th attempt complete")

x = range(0, 1000)
y1 = countR
y2 = countRR

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(x, y1, color='blue', label='Reservoir')
ax1.set_title('Reservoir')
ax1.legend()

ax2.plot(x, y2, color='red', label='Reservoir with Replacement')
ax2.set_title('Reservoir with Replacement')
ax2.legend()

plt.tight_layout()
plt.show()