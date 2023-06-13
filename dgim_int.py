import random
import matplotlib.pyplot as plt
import numpy as np

class Block:
    def __init__(self, size, t_start, t_end):
        self.size = size
        self.t_start = t_start
        self.t_end = t_end

    def __repr__(self):
        return f"{self.size, self.t_start, self.t_end}"

# 비트 단위로 나눠서 계산하기.
class DGIM_bit:
    def __init__(self):
        self.ts = 0
        self.dgim = [[[]],
                     [[]],
                     [[]],
                     [[]]]
        self.bitlen = 4

    def add(self, b): # b는 0~15 사이의 정수
        # ex) b = 14 -> b_arr = [1, 1, 1, 0]
        b_arr = []
        for i in range(self.bitlen):
            b_arr.append(b//2**(3-i))
            b = b%2**(3-i)
        
        for i in range(self.bitlen): # i: 0, 1, 2, 3
            if b_arr[i] == 0:
                pass
            else:
                self.dgim[i][0].append(Block(1, self.ts, self.ts))
                bi = 0
                while len(self.dgim[i][bi]) > 2:
                    b1 = self.dgim[i][bi].pop(0)
                    b2 = self.dgim[i][bi].pop(0)
                    new_block = Block(b1.size + b2.size,
                                      b1.t_start, 
                                      b2.t_end)
                    if len(self.dgim[i]) < bi + 2:
                        self.dgim[i].append([])
                    self.dgim[i][bi+1].append(new_block)
                    bi += 1
        self.ts += 1
        
    def count_bits(self, k):
        target_ts = self.ts - k
        cnt_arr = []
        ret = 0
        for i in range(self.bitlen): # i: 0, 1, 2, 3
            cnt = 0
            for blocks in self.dgim[i]:
                for b in reversed(blocks):
                    if target_ts <= b.t_start:
                        cnt += b.size
                    elif target_ts <= b.t_end:
                        cnt += b.size * ((b.t_end - target_ts + 1) / (b.t_end - b.t_start + 1))
                    else:
                        break
                else:
                    continue
                break
            cnt_arr.append(cnt)

        for i in range(self.bitlen): # 3-i: 3, 2, 1, 0
            ret += cnt_arr[i] * 2**(3-i)
        return ret

# 부분 합 유지하기.
class DGIM:
    def __init__(self):
        self.ts = 0
        self.dgim = [[]]

    def add(self, b): # b는 0~15 사이의 정수
        if b == 0:
            pass
        else:
            self.dgim[0].append(Block(b, self.ts, self.ts))
            bi = 0
            while len(self.dgim[bi]) > 2: # bi = 0
                if self.dgim[bi][0].size + self.dgim[bi][1].size > 2**(bi+1):
                    b1 = self.dgim[bi].pop(0)
                    new_block = b1
                else:
                    b1 = self.dgim[bi].pop(0)
                    b2 = self.dgim[bi].pop(0)
                    new_block = Block(b1.size + b2.size,
                                    b1.t_start,
                                    b2.t_end)
                
                if len(self.dgim) < bi + 2: #길이 짧으면 담을 바구니 생성.
                    self.dgim.append([])
                self.dgim[bi+1].append(new_block)
                bi += 1
        self.ts += 1

    def count_bits(self, k):
        target_ts = self.ts - k
        cnt = 0
        for blocks in self.dgim:
            for b in reversed(blocks):
                if target_ts <= b.t_start:
                    cnt += b.size
                elif target_ts <= b.t_end:
                    cnt += b.size * ((b.t_end - target_ts + 1) / (b.t_end - b.t_start + 1))
                else:
                    break
            else:
                continue
            break

        return cnt

dgim_bit = DGIM_bit()
dgim = DGIM()

# 제대로 동작하나 확인.
istream = [random.randrange(16) for _ in range(10000)]

for ts, b in enumerate(istream):
    dgim_bit.add(b)
    print(ts, b, dgim_bit.dgim)

for ts, b in enumerate(istream):
    dgim.add(b)
    print(ts, b, dgim.dgim)

#
x = range(1, 2000)
y1 = []
y2 = []
y3 = []
for k in range(1, 2000):
    y1.append(sum(istream[-k:]))
    y2.append(dgim_bit.count_bits(k))
    y3.append(dgim.count_bits(k))
    print(k, sum(istream[-k:]), dgim_bit.count_bits(k), dgim.count_bits(k))

plt.plot(x, y1, color='blue', label='Actual sum')
plt.plot(x, y2, color='red', label='first method')
plt.plot(x, y3, color='green', label='second method')

plt.legend()
plt.show()
