import math
import mmh3
import random
import string

class BloomFilter:
    def __init__(self, m, fp):
        self.k = int(math.ceil(- math.log2(fp)))
        self.n = int(self.k*m/math.log(2))
        self.B = 0
        self.seeds = [random.randrange(0, 100000) for _ in range(self.k)]
    
    def add(self, x):
        for i in range(self.k):
            idx = mmh3.hash(x, self.seeds[i]) % self.n
            self.B |= (1 << idx)
    
    def check(self, x):
        for i in range(self.k):
            idx = mmh3.hash(x, self.seeds[i]) % self.n
            if ((self.B >> idx) & 1) == 0:
                return False
        
        return True
    
bf = BloomFilter(20, 0.1)
cstream = [random.choice(string.ascii_letters) for _ in range(10)]
print(cstream)
for c in cstream:
    bf.add(c)

test_stream = [random.choice(string.ascii_letters) for _ in range(10000000)]
total = 0
cnt = 0
for t in test_stream:
    if bf.check(t) == True and t not in cstream:
        cnt += 1
    elif bf.check(t) == True:
        total += 1

f_p = cnt / total
print(f_p)