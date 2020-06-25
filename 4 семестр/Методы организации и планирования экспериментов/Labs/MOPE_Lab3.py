import math
import numpy as np
import random
import crit

k = 3
N = 4
m = 3
p = 0.95
x = [[-25, -5],
     [-30, 45],
     [-5, 5]]

x_av_max = sum([row[1] for row in x])/3
x_av_min = sum([row[0] for row in x])/3

y_max = 200+x_av_max
y_min = 200+x_av_min

x_norm = [[1, -1, -1, -1],
          [1, -1, -1, 1],
          [1, -1, 1, 1],
          [1, 1, 1, 1]]

x_norm_t = np.transpose(x_norm)
#print("x_norm:",x_norm)
x_nat = []
for i in range(N):
    x_nat.append([1])
    for j in range(1, k+1):
        if x_norm[i][j] < 0:
            x_nat[i].append(x[j - 1][0])
        else:
            x_nat[i].append(x[j - 1][1])

x_nat_t = list(np.transpose(x_nat))
x_nat_t.pop(0)

y = [[random.randint(y_min, y_max) for j in range(m)] for i in range(N)]

y_av = [sum(row)/m for row in y]

mx = [sum(x_nat_t[i])/N for i in range(k)]
my = sum(y_av)/N

a = []
for i in range(k):
    a.append([])
    for j in range(k):
        a[i].append(sum([a*b for (a,b) in zip(x_nat_t[i],x_nat_t[j])])/N)
a0 = [sum([a*b for a,b in zip(x_nat_t[i],y_av)])/N for i in range(k)]

left = [[1, mx[0], mx[1], mx[2]]]
for i in range(k):
    left.append([mx[i]])
    for j in range(k):
        left[i+1].append(a[j][i])

right = a0.copy()
right.insert(0, my)

b = np.linalg.solve(left, right)

# Print
head = "  | {:>3} {:>3} {:>3} |".format("X1", "X2", "X3")
for i in range(m):
    head += " {:>3}".format("Y{}".format(i+1))
head += " | {:>6} |".format("Y_av")
print(head)
for i in range(N):
    s = " {}| {:3} {:3} {:3} |".format(i+1, x_nat[i][1], x_nat[i][2], x_nat[i][3])
    for j in range(m):
        s += " {:.0f}".format(y[i][j])
    s += " | {:.2f} |".format(y_av[i])
    print(s)
rivn = " {:.3f}".format(b[0])
for i in range(1, k+1):
    if b[i] < 0:
        sign = "-"
    else:
        sign = "+"
    rivn += " {} {:.3f}*x{}".format(sign, abs(b[i]), i)
print("Рівняння регресії: у ="+rivn)

# Kohren
s2 = [sum([(y_av[i]-y[i][j])**2 for j in range(m)])/m for i in range(N)]

s2_max = max(s2)
Gp = s2_max/sum(s2)

f1 = m-1
f2 = N
q = 1 - p
G_cr = 7.679
if crit.Criteria.cohren(m, N, y_av, y):
    print("Дисперсії однорідні з ймовірнітю p = {}".format(p))
else:
    print("Дисперсії неоднорідні")

# Student
S2B = sum(s2)/N

S2_beta = S2B/(N*m)
S_beta = math.sqrt(S2_beta)

beta = [sum([x_norm_t[i][j]*y_av[j] for j in range(N)])/N for i in range(k+1)]

t = [abs(beta[i])/S_beta for i in range(N)]
f3 = (m-1)*N
t_table = 2.306
t_main = crit.Criteria.student(m, N, y_av, y, x_norm_t, k)
b_main = [b[i]*t_main[i] for i in range(k+1)]
rivn = ""
for i in range(k+1):
    if b[i] < 0:
        sign = "-"
    else:
        sign = "+"
    if t_main[i] == 1:
        if i == 0:
            rivn += " {} {:.3f}".format(sign, abs(b[i]))
        else:
            rivn += " {} {:.3f}*x{}".format(sign, abs(b[i]), i)
if rivn != "":
    rivn = rivn[2:]
print("Рівняння регресії із значущими коефіцієнтами: у ="+rivn)

# Fisher
d = sum(t_main)
y_main = [sum([a*b for (a,b) in zip(b_main, x_nat[i])]) for i in range(N)]
if d < k+1:
    F_cr = [-1, 5.3, 4.5, 4.1, 3.8, 3.7, 3.6]
    f4 = N - d
    S2_ad = m/f4*sum([(y_main[i]-y_av[i])**2 for i in range(N)])
    F = S2_ad/S2B
    if F < F_cr[f4]:
        print("Модель адекватна з ймовірнітю p = {}".format(p))
    else:
        print("Модель неадекватна")
else:
    print("Модель адекватна з ймовірнітю p = {}".format(p))

