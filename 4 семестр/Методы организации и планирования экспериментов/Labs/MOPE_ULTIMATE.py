import matplotlib.pyplot as plt
import numpy as np
import random
import crit
k = [3, 7, 10]
N = [4, 8, 14]

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

x_norm_comb = [[1, -1, -1, -1],
              [1, -1, -1, 1],
              [1, -1, 1, -1],
              [1, -1, 1, 1],
              [1, 1, -1, -1],
              [1, 1, -1, 1],
              [1, 1, 1, -1],
              [1, 1, 1, 1]]

x_norm_square = [[1, -1, -1, -1],
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
              [1, 0, 0, 1.215],]


def count_nat_simple():
    nat = []
    for i in range(N[0]):
        nat.append([1])
        for j in range(1, k[0]+1):
            if x_norm_simple[i][j] < 0:
                nat[i].append(x[j - 1][0])
            else:
                nat[i].append(x[j - 1][1])
    return nat


def count_nat_comb():
    nat = []
    for i in range(N[1]):
        nat.append([1])
        for j in range(1, k[0] + 1):
            if x_norm_comb[i][j] < 0:
                nat[i].append(x[j - 1][0])
            else:
                nat[i].append(x[j - 1][1])
    for i in range(N[1]):
        x_norm_comb[i].append(x_norm_comb[i][1] * x_norm_comb[i][2])
        x_norm_comb[i].append(x_norm_comb[i][1] * x_norm_comb[i][3])
        x_norm_comb[i].append(x_norm_comb[i][2] * x_norm_comb[i][3])
        x_norm_comb[i].append(x_norm_comb[i][1] * x_norm_comb[i][2] * x_norm_comb[i][3])

        nat[i].append(nat[i][1] * nat[i][2])
        nat[i].append(nat[i][1] * nat[i][3])
        nat[i].append(nat[i][2] * nat[i][3])
        nat[i].append(nat[i][1] * nat[i][2] * nat[i][3])
    return nat


x0 = [sum(row)/2 for row in x]
delta_x = [x[i][1] - x0[i] for i in range(k[0])]


def count_nat_square():
    nat = []
    for i in range(N[2]):
        nat.append([1])
        for j in range(1, k[0] + 1):
            if x_norm_square[i][j] == -1:
                nat[i].append(x[j - 1][0])
            elif x_norm_square[i][j] == 1:
                nat[i].append(x[j - 1][1])
            elif x_norm_square[i][j] == 0:
                nat[i].append(x0[j - 1])
            else:
                nat[i].append(x_norm_square[i][j] * delta_x[j - 1] + x0[j - 1])

    for i in range(N[2]):
        x_norm_square[i].append(x_norm_square[i][1] * x_norm_square[i][2])
        x_norm_square[i].append(x_norm_square[i][1] * x_norm_square[i][3])
        x_norm_square[i].append(x_norm_square[i][2] * x_norm_square[i][3])
        x_norm_square[i].append(x_norm_square[i][1] * x_norm_square[i][2] * x_norm_square[i][3])
        x_norm_square[i].append(x_norm_square[i][1] * x_norm_square[i][1])
        x_norm_square[i].append(x_norm_square[i][2] * x_norm_square[i][2])
        x_norm_square[i].append(x_norm_square[i][3] * x_norm_square[i][3])

        nat[i].append(nat[i][1] * nat[i][2])
        nat[i].append(nat[i][1] * nat[i][3])
        nat[i].append(nat[i][2] * nat[i][3])
        nat[i].append(nat[i][1] * nat[i][2] * nat[i][3])
        nat[i].append(nat[i][1] * nat[i][1])
        nat[i].append(nat[i][2] * nat[i][2])
        nat[i].append(nat[i][3] * nat[i][3])
    return nat


def print_simple_results(x_nat, b, t_main):
    head = "  | {:>3} {:>3} {:>3} |".format("X1", "X2", "X3")
    for i in range(cur_m):
        head += " {:>3}".format("Y{}".format(i + 1))
    head += " | {:>6} |".format("Y_av")
    print(head)
    for i in range(N[0]):
        s = " {}| {:3} {:3} {:3} |".format(i + 1, x_nat[i][1], x_nat[i][2], x_nat[i][3])
        for j in range(cur_m):
            s += " {:.0f}".format(y[i][j])
        s += " | {:.2f} |".format(y_av[i])
        print(s)
    rivn = " {:.3f}".format(b[0])
    for i in range(1, k[0] + 1):
        if b[i] < 0:
            sign = "-"
        else:
            sign = "+"
        rivn += " {} {:.3f}*x{}".format(sign, abs(b[i]), i)
    print("Рівняння регресії: у =" + rivn)
    print("Дисперсії однорідні з ймовірнітю p = {}".format(p))
    rivn_main = ""
    for i in range(k[0] + 1):
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
    for i in range(N[1]):
        s = " {}| ".format(i+1)
        for j in range(1, k[1]+1):
            s += "{:6} ".format(x_nat[i][j])
        s += "|"
        for j in range(cur_m):
            s += " {:.0f}".format(y[i][j])
        s += " | {:.2f} |".format(y_av[i])
        print(s)
    rivn = " {:.3f}".format(b[0])
    for i in range(1, k[1] + 1):
        if b[i] < 0:
            sign = "-"
        else:
            sign = "+"
        rivn += " {} {:.3f}*x{}".format(sign, abs(b[i]), i)
    print("Рівняння регресії: у =" + rivn)
    print("Дисперсії однорідні з ймовірнітю p = {}".format(p))
    rivn_main = ""
    for i in range(k[1] + 1):
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


def print_square_results(x_nat, b, t_main):
    head = "   | {:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8} |".format("X1", "X2", "X3", "X1X2", "X1X3", "X2X3", "X1X2X3", "X1^2", "X2^2", "X3^2")
    for i in range(cur_m):
        head += " {:>5}".format("Y{}".format(i + 1))
    head += " | {:>8} |".format("Y_av")
    print(head)
    for i in range(N[2]):
        s = " {:>2}| ".format(i+1)
        for j in range(1, k[2]+1):
            s += "{:8.2f} ".format(x_nat[i][j])
        s += "|"
        for j in range(cur_m):
            s += " {:5.0f}".format(y[i][j])
        s += " | {:8.2f} |".format(y_av[i])
        print(s)
    rivn = " {:6.3f}".format(b[0])
    for i in range(1, k[2] + 1):
        if b[i] < 0:
            sign = "-"
        else:
            sign = "+"
        rivn += " {} {:.3f}*x{}".format(sign, abs(b[i]), i)
    print("\nРівняння регресії: у =" + rivn)
    print("Дисперсії однорідні з ймовірнітю p = {}".format(p))
    rivn_main = " {:6.3f}".format(b[0]) if t_main[0] > 0 else ""
    for i in range(1, k[2] + 1):
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
        rivn_main = rivn_main[1:]
    print("Рівняння регресії із значущими коефіцієнтами: у = " + rivn_main)
    print("Модель адекватна з ймовірнітю p = {}".format(p))


def solve(k, N, x_nat_t):
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


x_nat_simple = count_nat_simple()
x_nat_comb = count_nat_comb()
x_nat_square = count_nat_square()

x_nat = [x_nat_simple, x_nat_comb, x_nat_square]
x_norm = [x_norm_simple, x_norm_comb, x_nat_square]
results = [print_simple_results, print_comb_results, print_square_results]
b_start = [8.6, 6.5, 9.5, 4.2, 0.6, 0.2, 5.9, 3.9, 8.0, 0.5, 2.3]
wrong = ["Модель неадекватна, переходимо до регресії з  урахованням ефекту взаємодії",
         "Модель неадекватна, переходимо до регресії з урахованням квадратичних членів",
         "Модель неадекватна, перераховуємо y"]

dispersion = 5
while cur_m < crit.max_m:
    done = False
    print("m = {}".format(cur_m))
    for regr_type in range(3):
        nat = x_nat[regr_type]
        nat_t = list(np.transpose(nat))
        nat_t.pop(0)
        norm = x_norm[regr_type]
        norm_t = np.transpose(norm)
        y = [[sum([(a * c) for a, c in zip(nat[i], b_start[:k[regr_type]+1])]) + random.randint(0, dispersion) for j in range(cur_m)]
             for i in range(N[regr_type])]
        # y = [[random.randint(y_min, y_max) for j in range(cur_m)] for i in range(N[regr_type])]
        y_av = [sum(row) / cur_m for row in y]

        b = solve(k[regr_type], N[regr_type], nat_t)

        if not crit.Criteria.cohren(cur_m, N[regr_type], y_av, y):
            cur_m += 1
            print("Дисперсії неоднорідні, збільшуємо m")
            break

        t_main = crit.Criteria.student(cur_m, N[regr_type], y_av, y, norm_t, k[regr_type])
        b_main = [b[i] * t_main[i] for i in range(k[regr_type] + 1)]

        if crit.Criteria.fisher(cur_m, N[regr_type], y_av, y, t_main, b_main, nat, k[regr_type]):
            results[regr_type](nat, b, t_main)
            done = True
            break
        print(wrong[regr_type])
    cur_m = 3
    if done:
        break

