import math

f = 0.0010732
x_left = [-0.5]
a_left = []
h_left = []
x_right = [0.5]
a_right = []
h_right = []
n_left = 6
n_right = 9 - n_left

# f_test = 0
# dif = 100
# f_dif = 0
# while f_test < 0.007:
#     x_left = [-0.5]
#     a_left = []
#     h_left = []
#     x_right = [0.5]
#     a_right = []
#     h_right = []
#     for i in range(n_left-1):
#         a = abs(-math.exp(-x_left[i])*(x_left[i]-2))
#         a_left.append(a)
#         h_left.append(math.sqrt(16*f_test/a))
#         x_left.append(x_left[i] + h_left[i])
#     a = abs(-math.exp(-x_left[-1]) * (x_left[-1] - 2))
#     a_left.append(a)
#     h_left.append(math.sqrt(8 * f_test / a))
#     x_left.append(x_left[-1] + h_left[-1])
#
#     for i in range(n_right - 1):
#         a = abs(-x_right[i]/math.pow((1-x_right[i]*x_right[i]), 1.5))
#         a_right.append(a)
#         h_right.append(math.sqrt(16 * f_test / a))
#         x_right.append(x_right[i] - h_right[i])
#     a = abs(-x_right[-1]/math.pow((1-x_right[-1]*x_right[-1]), 1.5))
#     a_right.append(a)
#     h_right.append(math.sqrt(8 * f_test / a))
#     x_right.append(x_right[-1] - h_right[-1])
#
#     dif_test = max(abs(x_left[-1]), abs(x_right[-1]))
#     if dif_test < dif:
#         dif = dif_test
#         f_dif = f_test
#
#     f_test += 0.0000001
# print(dif)
# print(f_dif)

for i in range(n_left - 1):
    a = abs(-math.exp(-x_left[i]) * (x_left[i] - 2))
    a_left.append(a)
    h_left.append(math.sqrt(16 * f / a))
    x_left.append(x_left[i] + h_left[i])
a = abs(-math.exp(-x_left[-1]) * (x_left[-1] - 2))
a_left.append(a)
h_left.append(math.sqrt(8 * f / a))
x_left.append(x_left[-1] + h_left[-1])
for i in range(n_right - 1):
    a = abs(-math.exp(-x_right[i]) * (x_right[i] - 2))
    a_right.append(a)
    h_right.append(math.sqrt(16 * f / a))
    x_right.append(x_right[i] - h_right[i])
a = abs(-x_right[-1] / math.pow((1 - x_right[-1] * x_right[-1]), 1.5))
a_right.append(a)
h_right.append(math.sqrt(8 * f / a))
x_right.append(x_right[-1] - h_right[-1])

print(x_left)
print(a_left)
print(h_left)
print()
print(x_right)
print(a_right)
print(h_right)



