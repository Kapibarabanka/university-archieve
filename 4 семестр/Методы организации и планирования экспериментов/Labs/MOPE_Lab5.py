import numpy as np
import random
import crit

k_simple = 3
k = 10
N = 15
cur_m = 3
p = 0.95
x = [[-4, 3],
     [-6, 10],
     [0, 3]]

x_av_max = sum([row[1] for row in x]) / k_simple
x_av_min = sum([row[0] for row in x]) / k_simple

y_max = round(200+x_av_max)
y_min = round(200+x_av_min)


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


def print_results(x_nat, b, t_main):
    head = "   | {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} {:>7} |".format("X1", "X2", "X3", "X1X2", "X1X3", "X2X3", "X1X2X3", "X1^2", "X2^2", "X3^2")
    for i in range(cur_m):
        head += " {:>3}".format("Y{}".format(i + 1))
    head += " | {:>6} |".format("Y_av")
    head += " | {:>6} |".format("Y_t1")
    head += " {:>6} |".format("Y_t2")
    print(head)
    for i in range(N):
        s = " {:>2}| ".format(i+1)
        for j in range(1, k+1):
            s += "{:7.2f} ".format(x_nat[i][j])
        s += "|"
        for j in range(cur_m):
            s += " {:.0f}".format(y[i][j])
        s += " | {:.2f} |".format(y_av[i])
        s += " | {:.2f} |".format(y_test1[i])
        s += " {:.2f} |".format(y_test2[i])
        print(s)
    rivn = " {:6.3f}".format(b[0])
    for i in range(1, k + 1):
        if b[i] < 0:
            sign = "-"
        else:
            sign = "+"
        rivn += " {} {:.3f}*x{}".format(sign, abs(b[i]), i)
    print("\nРівняння регресії: у =" + rivn)
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


x_norm = [[1, -1, -1, -1],
          [1, -1, -1, 1],
          [1, -1, 1, -1],
          [1, -1, 1, 1],
          [1, 1, -1, -1],
          [1, 1, -1, 1],
          [1, 1, 1, -1],
          [1, 1, 1, 1],
          [1, -1.215, 0, 0],
          [1, 1.215, 0, 0],
          [1, 0, -1.215, 0],
          [1, 0, 1.215, 0],
          [1, 0, 0, -1.215],
          [1, 0, 0, 1.215],
          [1, 0, 0, 0]]

x0 = [sum(row)/2 for row in x]
delta_x = [x[i][1] - x0[i] for i in range(k_simple)]

x_nat = []
for i in range(N):
    x_nat.append([1])
    for j in range(1, k_simple + 1):
        if x_norm[i][j] == -1:
            x_nat[i].append(x[j - 1][0])
        elif x_norm[i][j] == 1:
            x_nat[i].append(x[j - 1][1])
        elif x_norm[i][j] == 0:
            x_nat[i].append(x0[j - 1])
        else:
            x_nat[i].append(x_norm[i][j]*delta_x[j - 1] + x0[j-1])

for i in range(N):
    x_norm[i].append(x_norm[i][1] * x_norm[i][2])
    x_norm[i].append(x_norm[i][1] * x_norm[i][3])
    x_norm[i].append(x_norm[i][2] * x_norm[i][3])
    x_norm[i].append(x_norm[i][1] * x_norm[i][2] * x_norm[i][3])
    x_norm[i].append(x_norm[i][1] * x_norm[i][1])
    x_norm[i].append(x_norm[i][2] * x_norm[i][2])
    x_norm[i].append(x_norm[i][3] * x_norm[i][3])

    x_nat[i].append(x_nat[i][1] * x_nat[i][2])
    x_nat[i].append(x_nat[i][1] * x_nat[i][3])
    x_nat[i].append(x_nat[i][2] * x_nat[i][3])
    x_nat[i].append(x_nat[i][1] * x_nat[i][2] * x_nat[i][3])
    x_nat[i].append(x_nat[i][1] * x_nat[i][1])
    x_nat[i].append(x_nat[i][2] * x_nat[i][2])
    x_nat[i].append(x_nat[i][3] * x_nat[i][3])

x_norm_t = np.transpose(x_norm)
x_nat_t = list(np.transpose(x_nat))
x_nat_t.pop(0)

while cur_m < crit.max_m:
    print("m = {}".format(cur_m))
    y = [[random.randint(y_min, y_max) for j in range(cur_m)] for i in range(N)]
    y_av = [sum(row) / cur_m for row in y]

    if not crit.Criteria.cohren(cur_m, N, y_av, y):
        cur_m += 1
        print("Дисперсії неоднорідні, збільшуємо m")
        continue

    b = solve(k, N)

    t_main = crit.Criteria.student(cur_m, N, y_av, y, x_norm_t, k)
    b_main = [b[i] * t_main[i] for i in range(k + 1)]

    y_test1 = [sum([(a * c) for a, c in zip(x_nat[i], b)]) for i in range(N)]
    y_test2 = [sum([(a * c) for a, c in zip(x_nat[i], b_main)]) for i in range(N)]

    if crit.Criteria.fisher(cur_m, N, y_av, y, t_main, b_main, x_nat, k):
        print_results(x_nat, b, t_main)
        break
    print("Модель неадекватна, збільшуємо m")
    cur_m += 1
