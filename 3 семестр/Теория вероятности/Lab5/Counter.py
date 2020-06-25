import math
import numpy as np
import random

N = 3
paths = [[0, 2, 1],
         [0, 0, 0.5],
         [0.25, 0, 0]]

coeffs = [[1, 1, 1],
          [0, 0, 0],
          [0, 0, 0]]

for i in range(1,3):
    for j in range(N):
        if j != i:
            coeffs[i][j] += paths[j][i]
            coeffs[i][i] -= paths[i][j]

matrix = np.array(coeffs)
vector = np.array([1., 0., 0.])
result_teor = list(np.linalg.solve(matrix, vector))

total = 0
totalV = [0, 0, 0]
jumpTo = 0
prevJump = 0
t = [0,0,0]
result_exp = [0, 0, 0]
for i in range(1000):
    total += t[jumpTo]
    totalV[prevJump] += t[jumpTo]
    prevJump = jumpTo
    for j in range(N):
        if paths[jumpTo][j] != 0:
            t[j] = (-1/paths[jumpTo][j])*math.log(random.random())
        else:
            t[j] = 100000
    jumpTo = 0
    for j in range(1, N):
        if t[j] == min(t):
            jumpTo = j
            break
for i in range(N):
    result_exp[i] = totalV[i]/total

print("Теоретичні значення:")
print("\tP1 = {0}\n\tP2 = {1}\n\tP3 = {2}".format(*result_teor))
print("Експерементальні значення:")
print("\tP1 = {0}\n\tP2 = {1}\n\tP3 = {2}".format(*result_exp))