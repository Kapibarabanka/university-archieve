import math
import Counter

counter = Counter.Counter()
counter.a = 0
counter.b = 0.5
counter.c = 0.75
counter.d = 1.25
counter.h1= 0.4
counter.h2 = 2
counter.h3 = 0.6
if not counter.count_areas():
    print("Сумма площадей ступенек не равна 1")
elif not counter.right_order():
    print("Числа введены в неправильном порядке\nДолжно быть: a< b < c < d")
else:
    print(counter.count())
