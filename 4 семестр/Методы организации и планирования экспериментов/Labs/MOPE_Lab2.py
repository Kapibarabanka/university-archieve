import numpy as np
import random

table = {
    (2, 0.9): 1.69,
    (2, 0.95): 1.71,
    (2, 0.98): 1.72,
    (2, 0.99): 1.73,
    (6, 0.9): 2.0,
    (6, 0.95): 2.1,
    (6, 0.98): 2.13,
    (6, 0.99): 2.16,
    (8, 0.9): 2.17,
    (8, 0.95): 2.27,
    (8, 0.98): 2.37,
    (8, 0.99): 2.43,
    (10, 0.9): 2.29,
    (10, 0.95): 2.41,
    (10, 0.98): 2.54,
    (10, 0.99): 2.62,
    (12, 0.9): 2.39,
    (12, 0.95): 2.52,
    (12, 0.98): 2.66,
    (12, 0.99): 2.75,
    (15, 0.9): 2.49,
    (15, 0.95): 2.64,
    (15, 0.98): 2.8,
    (15, 0.99): 2.9,
    (20, 0.9): 2.62,
    (20, 0.95): 2.78,
    (20, 0.98): 2.96,
    (20, 0.99): 3.08
}
pos_m = sorted(list(set([i[0] for i in list(table.keys())])))
var = 10
x1_min = -25
x1_max = -5
del_x1 = abs(x1_max-x1_min)/2
x10 = (x1_max+x1_min)/2
x2_min = -30
x2_max = 45
del_x2 = abs(x2_max-x2_min)/2
x20 = (x2_max+x2_min)/2
N = 3
y_max = (30-var)*10
y_min = (20-var)*10

cur_m = pos_m[0]
p = 0.99

x_min = -1
x_max = 1
x = [[x_min, x_min],
     [x_min, x_max],
     [x_max, x_max]]


def exp_y(m):
    y = np.zeros((N, m))
    for row in range(N):
        for el in range(m):
            y[row][el] = int(random.randint(y_min, y_max))

    y_av = [sum(y[row])/m for row in range(N)]

    sigm = [sum([(y[row][i]-y_av[row])**2 for i in range(m)])/m for row in range(N)]

    sigm_main = np.sqrt((4*m-4)/m/(m-4))

    F_uv = []
    for i in range(N-1):
        for j in range(i+1, N):
            if sigm[i] >= sigm[j]:
                F_uv.append(sigm[i]/sigm[j])
            else:
                F_uv.append(sigm[j]/sigm[i])

    theta_uv = [(m-2)/m*F_uv[i] for i in range(N)]

    R_uv = [abs(theta_uv[i]-1)/sigm_main for i in range(N)]

    return {"y": y, "y_av": y_av, "R_uv": R_uv}


def romanovski(m , p):
    return table[(m,p)]


temp = {}
while cur_m <= max(pos_m):
    cur_m = pos_m[pos_m.index(cur_m) + 1]
    print("m =", cur_m)
    temp = exp_y(cur_m)
    R_cr = romanovski(cur_m, p)
    flag = True
    for i in temp["R_uv"]:
        if i > R_cr:
            flag = False
            break
    if flag:
        break
    if cur_m == max(pos_m):
        print("У таблиці немає значень Rкр для m > 20")

y = temp["y"]
y_av = temp["y_av"]
mx1 = sum([i[0] for i in x])/N
mx2 = sum([i[1] for i in x])/N
my = sum(y_av)/N
a1 = sum([i[0]**2 for i in x])/N
a2 = sum([i[0]*i[1] for i in x])/N
a3 = sum([i[1]**2 for i in x])/N
a11 = sum([x[i][0]*y_av[i] for i in range(N)])/N
a22 = sum([x[i][1]*y_av[i] for i in range(N)])/N

a = [
    [1, mx1, mx2],
    [mx1, a1, a2],
    [mx2, a2, a3]
]
z = [my, a11, a22]
b = np.linalg.solve(a, z)
y_b = [b[0]+x[i][0]*b[1]+x[i][1]*b[2] for i in range(N)]

x_nat = []
for i in range(N):
    x_nat.append([(x1_min if x[i][0] == x_min else x1_max), (x2_min if x[i][1] == x_min else x2_max)])
a0 = b[0]-b[1]*x10/del_x1-b[2]*x20/del_x2
a1 = b[1]/del_x1
a2 = b[2]/del_x2
y_a = [a0+x_nat[i][0]*a1+x_nat[i][1]*a2 for i in range(N)]

str = "  | {:>3} {:>3} |".format("X1n", "X2n")
for i in range(cur_m):
    str += " {:>3}".format("Y{}".format(i+1))
str += " |"
print(str)
for i in range(N):
    s = " {}| {:3} {:3} |".format(i+1, *x[i])
    for j in range(cur_m):
        s += " {:.0f}".format(y[i][j])
    s += " |"
    print(s)
print("Рівняння регресії з нормованими коефіцієнтами: y = {:.3f} + {:.3f}*x1n + {:.3f}*x2n".format(*b))
print("   | {:>3} {:>3} | {:>7} | {:>7} |".format("X1n", "X2n", "y_av", "y(b)"))
for i in range(N):
    print(" {} | {:3} {:3} | {:5.3f} | {:5.3f} |".format(i+1, x[i][0], x[i][1], y_av[i], y_b[i]))
print("Рівняння регресії з натуралізованими коефіцієнтами: y = {:.3f} + {:.3f}*x1 + {:.3f}*x2".format(a0, a1, a2))
print("   | {:>4} {:>4} | {:>7} | {:>7} |".format("X1", "X2", "y_av", "y(a)"))
for i in range(N):
    print(" {} | {:4} {:4} | {:5.3f} | {:5.3f} |".format(i+1, x_nat[i][0], x_nat[i][1], y_av[i], y_a[i]))
