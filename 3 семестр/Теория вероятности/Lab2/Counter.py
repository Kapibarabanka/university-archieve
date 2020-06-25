import random
import math


class Counter:
    h1 = 0.4
    h2 = 2
    h3 = 0.6
    a = 0
    b = 0.5
    c = 0.75
    d = 1.25
    s1 = math.fabs(a-b)*h1
    s2 = math.fabs(b-c)*h2
    s3 = math.fabs(c-d)*h3
    quantity = 5000

    def right_order(self):
        return self.a <= self.b and self.b <= self.c and self.c <= self.d

    # Считает площади ступенек и проверяет, равна ли их сумма 1
    def count_areas(self):
        self.s1 = math.fabs(self.a - self.b) * self.h1
        self.s2 = math.fabs(self.b - self.c) * self.h2
        self.s3 = math.fabs(self.c - self.d) * self.h3
        return self.s1+self.s2+self.s3 == 1

    # Высчитывает R в зависимости от случайного r
    def generate(self, r):
        if r <= self.s1:
            return self.a+ r/ self.h1
        elif r <= self.s1+self.s2:
            return self.b+ (r-self.s1)/self.h2
        else:
            return self.c + (r-self.s1-self.s2)/self.h3

    # Рассчитывает теоретическое значение математического ожидания
    def theor_expected(self):
        return 0.5 * (self.h1*(self.b**2 - self.a**2) + self.h2*(self.c**2 - self.b**2) + self.h3*(self.d**2 - self.c**2))

    # Рассчитывает теоретическое значение среднеквадратичного отлонения
    def theor_deviation(self, m):
        return ( self.h1*(self.b**3 - self.a**3) + self.h2*(self.c**3 - self.b**3) + self.h3*(self.d**3 - self.c**3)) / 3 - m**2

    # Рассчитывает эксперементальное значение математического ожидания
    def expected(self, numbers):
        return sum(numbers)/self.quantity

    # Рассчитывает эксперементальное значение среднеквадратичного отлонения
    def deviation(self, numbers, m):
        return sum(map(lambda x: x*x, numbers)) / self.quantity - m**2

    # Генерирует массив из 5000 чисел по заданному закону,
    # рассчитывает теоретические и эксперементальные значения математического ожидания и среднеквадратичного отлонения
    def count(self):
        numbers = []
        for i in range(self.quantity):
            r = random.random()
            numbers.append(self.generate(r))
        tm = self.theor_expected()
        td = self.theor_deviation(tm)
        pm = self.expected(numbers)
        pd = self.deviation(numbers, pm)
        return {"tm": tm, "td": td, "pm": pm, "pd": pd}
