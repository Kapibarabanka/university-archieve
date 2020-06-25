import math
import numpy as np
import random
import crit
k_simple = 3
k_comb = 7
N_simple = 4
N_comb = 8
cur_m = 3
p = 0.95

x = [[-20, 15],
     [10, 60],
     [15, 35]]

x_av_max = sum([row[1] for row in x])/3
x_av_min = sum([row[0] for row in x])/3

y_max = round(200+x_av_max)
y_min = round(200+x_av_min)

x_norm_simple = [[1, -1, -1, -1],
                  [1, -1, -1, 1],
                  [1, -1, 1, 1],
                  [1, 1, 1, 1]]
x_norm_t_simple = np.transpose(x_norm_simple)
x_norm_comb = [[1, -1, -1, -1],
              [1, -1, -1, 1],
              [1, -1, 1, -1],
              [1, -1, 1, 1],
              [1, 1, -1, -1],
              [1, 1, -1, 1],
              [1, 1, 1, -1],
              [1, 1, 1, 1]]

x_nat_simple = []
for i in range(N_simple):
    x_nat_simple.append([1])
    for j in range(1, k_simple+1):
        if x_norm_simple[i][j] < 0:
            x_nat_simple[i].append(x[j - 1][0])
        else:
            x_nat_simple[i].append(x[j - 1][1])

x_nat_t_simple = list(np.transpose(x_nat_simple))
x_nat_t_simple.pop(0)

x_nat_comb = []
for i in range(N_comb):
    x_nat_comb.append([1])
    for j in range(1, k_simple+1):
        if x_norm_comb[i][j] < 0:
            x_nat_comb[i].append(x[j - 1][0])
        else:
            x_nat_comb[i].append(x[j - 1][1])

for i in range(N_comb):
    x_norm_comb[i].append(x_norm_comb[i][1] * x_norm_comb[i][2])
    x_norm_comb[i].append(x_norm_comb[i][1] * x_norm_comb[i][3])
    x_norm_comb[i].append(x_norm_comb[i][2] * x_norm_comb[i][3])
    x_norm_comb[i].append(x_norm_comb[i][1] * x_norm_comb[i][2] * x_norm_comb[i][3])

    x_nat_comb[i].append(x_nat_comb[i][1] * x_nat_comb[i][2])
    x_nat_comb[i].append(x_nat_comb[i][1] * x_nat_comb[i][3])
    x_nat_comb[i].append(x_nat_comb[i][2] * x_nat_comb[i][3])
    x_nat_comb[i].append(x_nat_comb[i][1] * x_nat_comb[i][2] * x_nat_comb[i][3])

x_norm_t_comb = np.transpose(x_norm_comb)
x_nat_t_comb = list(np.transpose(x_nat_comb))
x_nat_t_comb.pop(0)
x_norm = []
x_nat = []
x_nat_t = []
x_norm_t = []
y = []
y_av = []

def print_results(x_nat, b, t_main):
    head = "  | {:>3} {:>3} {:>3} |".format("X1", "X2", "X3")
    for i in range(cur_m):
        head += " {:>3}".format("Y{}".format(i + 1))
    head += " | {:>6} |".format("Y_av")
    print(head)
    for i in range(N):
        s = " {}| {:3} {:3} {:3} |".format(i + 1, x_nat[i][1], x_nat[i][2], x_nat[i][3])
        for j in range(cur_m):
            s += " {:.0f}".format(y[i][j])
        s += " | {:.2f} |".format(y_av[i])
        print(s)
    rivn = " {:.3f}".format(b[0])
    for i in range(1, k + 1):
        if b[i] < 0:
            sign = "-"
        else:
            sign = "+"
        rivn += " {} {:.3f}*x{}".format(sign, abs(b[i]), i)
    print("Рівняння регресії: у =" + rivn)
    print("Дисперсії однорідні з ймовірнітю p = {}".format(p))
    rivn_main = ""
    for i in range(k + 1):
        if b[i] < 0:
            sign = "-"
        else:
            sign = "+"
        if t_main[i] == 1:
            if i == 0:
                rivn_main += " {} {:.3f}".format(sign, abs(b[i]))
            else:
                rivn_main += " {} {:.3f}*x{}".format(sign, abs(b[i]), i)
    if rivn_main != "":
        rivn_main = rivn_main[2:]
    print("Рівняння регресії із значущими коефіцієнтами: у =" + rivn_main)
    print("Модель адекватна з ймовірнітю p = {}".format(p))


def print_comb_results(x_nat, b, t_main):
    head = "  | {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} |".format("X1", "X2", "X3", "X1X2", "X1X3", "X2X3", "X1X2X3")
    for i in range(cur_m):
        head += " {:>3}".format("Y{}".format(i + 1))
    head += " | {:>6} |".format("Y_av")
    print(head)
    for i in range(N):
        s = " {}| ".format(i+1)
        for j in range(1, k_comb+1):
            s += "{:6} ".format(x_nat[i][j])
        s += "|"
        for j in range(cur_m):
            s += " {:.0f}".format(y[i][j])
        s += " | {:.2f} |".format(y_av[i])
        print(s)
    rivn = " {:.3f}".format(b[0])
    for i in range(1, k + 1):
        if b[i] < 0:
            sign = "-"
        else:
            sign = "+"
        rivn += " {} {:.3f}*x{}".format(sign, abs(b[i]), i)
    print("Рівняння регресії: у =" + rivn)
    print("Дисперсії однорідні з ймовірнітю p = {}".format(p))
    rivn_main = ""
    for i in range(k + 1):
        if b[i] < 0:
            sign = "-"
        else:
            sign = "+"
        if t_main[i] == 1:
            if i == 0:
                rivn_main += " {} {:.3f}".format(sign, abs(b[i]))
            else:
                rivn_main += " {} {:.3f}*x{}".format(sign, abs(b[i]), i)
    if rivn_main != "":
        rivn_main = rivn_main[2:]
    print("Рівняння регресії із значущими коефіцієнтами: у =" + rivn_main)
    print("Модель адекватна з ймовірнітю p = {}".format(p))


def solve(k, N):
    mx = [sum(x_nat_t[i]) / N for i in range(k)]
    my = sum(y_av) / N
    a = []
    for i in range(k):
        a.append([])
        for j in range(k):
            a[i].append(sum([float(a * b) for (a, b) in zip(x_nat_t[i], x_nat_t[j])]) / N)
    a0 = [sum([a * b for a, b in zip(x_nat_t[i], y_av)]) / N for i in range(k)]
    left = []
    left.append(mx.copy())
    left[0].insert(0, 1)
    for i in range(k):
        left.append([mx[i]])
        for j in range(k):
            left[i + 1].append(a[j][i])
    right = a0.copy()
    right.insert(0, my)
    return np.linalg.solve(left, right)

while cur_m < 6:
    print("m = {}".format(cur_m))
    x_nat = x_nat_simple
    x_nat_t = x_nat_t_simple
    x_norm = x_norm_simple
    x_norm_t = x_norm_t_simple
    N = N_simple
    k = k_simple
    y = [[random.randint(y_min, y_max) for j in range(cur_m)] for i in range(N)]
    y_av = [sum(row) / cur_m for row in y]

    b = solve(k, N)

    if not crit.Criteria.cohren(cur_m, N, y_av, y):
        cur_m += 1
        print("Дисперсії неоднорідні")
        continue

    t_main = crit.Criteria.student(cur_m, N, y_av, y, x_norm_t, k)
    b_main = [b[i] * t_main[i] for i in range(k + 1)]

    if crit.Criteria.fisher(cur_m, N, y_av, y, t_main, b_main, x_nat, k):
        print_results(x_nat, b, t_main)
        break
    print("Модель неадекватна, переходимо до регресії з ефектом взаємодії")

    # With interactions
    x_nat = x_nat_comb
    x_nat_t = x_nat_t_comb
    x_norm = x_norm_comb
    x_norm_t = x_norm_t_comb
    N = N_comb
    k = k_comb
    y = [[random.randint(y_min, y_max) for j in range(cur_m)] for i in range(N)]
    y_av = [sum(row) / cur_m for row in y]

    b = solve(k, N)

    if not crit.Criteria.cohren(cur_m, N, y_av, y):
        cur_m += 1
        print("Дисперсії неоднорідні")
        continue

    t_main = crit.Criteria.student(cur_m, N, y_av, y, x_norm_t, k)
    b_main = [b[i] * t_main[i] for i in range(k + 1)]

    if crit.Criteria.fisher(cur_m, N, y_av, y, t_main, b_main, x_nat, k):
        print_comb_results(x_nat, b, t_main)
        break
    print("Модель неадекватна, перераховуємо у")

