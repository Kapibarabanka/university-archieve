import math
import scipy.stats
import random


class Simpson:
    def __init__(self, m, a):
        self.m = m
        self.a = a
        self.h = 1/a
        self.left = self.m - self.a
        self.right = self.m + self.a

    def value(self, x):
        return self.h-self.h*self.h*math.fabs(x-self.m)

    def count_prob(self, x_from, x_to):
        if x_from < self.m < x_to:
            return 1 - 0.5*(x_from-self.m+1/self.h)*self.value(x_from)- 0.5*(self.m+1/self.h-x_to)*self.value(x_to)
        if x_from < self.m and x_to <= self.m:
            return 0.5*(x_to - self.left)*self.value(x_to) - 0.5*(x_from - self.left)*self.value(x_from)
        if x_to > self.m and x_from >= self.m:
            return 0.5 * (self.right - x_from) * self.value(x_from) - 0.5 * (self.right - x_to) * self.value(x_to)

    def generate(self):
        r = random.random()
        if r < 0.5:
            x = self.left
            while x < self.m:
                x += 0.001
                if self.count_prob(self.left, x) >= r:
                    return x
        else:
            x = self.m
            while x <= self.right:
                x += 0.001
                if self.count_prob(self.left, x) >= r:
                    return x


class Normal:
    def __init__(self, m, s):
        self.m = m
        self.s = s

    def value(self, x):
        return scipy.stats.norm(self.m, self.s).pdf(x)

    def laplas(self, x):
        return scipy.stats.norm(self.m, self.s).cdf(x)-0.5

    def count_prob(self, x_from, x_to):
        return self.laplas(x_to) - self.laplas(x_from)

    def generate(self):
        return random.normalvariate(self.m, self.s)


class Counter:
    def __init__(self, normal_m, normal_s, simps_m, simps_a, p_a_not_b=-1.0, p_b_not_a=-1.0, p=-1.0, c1=-1.0, c2=-1.0):
        self.n0 = Normal(normal_m, normal_s)
        self.s1 = Simpson(simps_m, simps_a)
        self.p1 = p_a_not_b
        self.p2 = p_b_not_a
        self.p = p
        self.c1 = c1
        self.c2 = c2
        self.left = self.s1.m - self.s1.a
        self.right = self.s1.m + self.s1.a
        self.step = 0.001
        self.section0 = []
        self.section1 =[]
        self.result_teor = "Теоретичні значення:"
        self.result_exp = "Експерементальні значення:"

    def find_y0_p1(self):
        y1 = self.left
        y2 = self.right
        flag = False
        if self.n0.m == self.s1.m:
            while (y2 >= self.left):
                if y1 < y2:
                    if self.n0.count_prob(self.left, y1) + self.n0.count_prob(y2, self.right) >=self.p1:
                        flag = True
                        break
                else:
                    if self.n0.count_prob(y2, y1) >=self.p1:
                        flag = True
                        break
                y1 += self.step
                y2 -= self.step
        elif self.n0.m < self.s1.m:
            while (y2 >= self.left):
                while (y1 <= self.right):
                    if y1 < y2:
                        if self.n0.count_prob(self.left, y1) + self.n0.count_prob(y2, self.right) >=self.p1:
                            flag = True
                            break
                    else:
                        if self.n0.count_prob(y2, y1) >=self.p1:
                            flag = True
                            break
                    y1 += self.step
                if (flag):
                    break
                y2 -= self.step
        else:
            while (y1 <= self.right):
                while (y2 >= self.left):
                    if y1 < y2:
                        if self.n0.count_prob(self.left, y1) + self.n0.count_prob(y2, self.right) >= self.p1:
                            flag = True
                            break
                    else:
                        if self.n0.count_prob(y2, y1) >= self.p1:
                            flag = True
                            break
                    y2 -= self.step
                if (flag):
                    break
                y1 += self.step

        self.section0 = [y1, y2]

    def find_y0_p2(self):
        y1 = self.left
        y2 = self.right
        flag = False
        if self.n0.m == self.s1.m:
            while (y2 >= self.left):
                if y1 < y2:
                    if self.s1.count_prob(y1, y2) <= self.p2:
                        flag = True
                        break
                else:
                    if self.s1.count_prob(self.left, y2) + self.s1.count_prob(y1, self.right) <= self.p1:
                        flag = True
                        break
                y1 += self.step
                y2 -= self.step
        elif self.n0.m < self.s1.m:
            while (y2 >= self.left):
                while (y1 <= self.right):
                    if y1 < y2:
                        if self.s1.count_prob(y1, y2) <= self.p2:
                            flag = True
                            break
                    else:
                        if self.s1.count_prob(self.left, y2) + self.s1.count_prob(y1, self.right) <= self.p1:
                            flag = True
                            break
                    y1 += self.step
                if (flag):
                    break
                y2 -= self.step
        else:
            while (y1 <= self.right):
                while (y2 >= self.left):
                    if y1 < y2:
                        if self.s1.count_prob(y1, y2) <= self.p2:
                            flag = True
                            break
                    else:
                        if self.s1.count_prob(self.left, y2) + self.s1.count_prob(y1, self.right) <= self.p1:
                            flag = True
                            break
                    y2 -= self.step
                if (flag):
                    break
                y1 += self.step
        self.section0 = [y1, y2]

    def find_y0_pirson(self):
        y = self.left+self.step
        y01 = self.left # начало нулевой
        y02 = self.right # конец нулевой
        flag = self.n0.value(y)/self.s1.value(y)<self.p*self.c1/(1-self.p)/self.c2
        while y < self.right:
            y += self.step
            if(flag):
                if not self.n0.value(y)/self.s1.value(y)<self.p*self.c1/(1-self.p)/self.c2 and y > self.left:
                    y02 = y
                    flag = False
            else:
                if self.n0.value(y)/self.s1.value(y)<self.p*self.c1/(1-self.p)/self.c2 and y < self.right:
                    y01 = y
                    flag = True
        self.section0 = (y01, y02)

    def make_sections(self):
        if self.section0[0] < self.section0[1]:
            self.section1 = self.section0.copy()
            if self.section1[0] == self.left:
                self.section0 = [self.section1[1], self.right]
            elif self.section1[1] == self.right:
                self.section0 = [self.left, self.section1[0]]
            else:
                self.section0 = [[self.left, self.section1[0]], [self.section1[1], self.right]]
        else:
            if self.section0[0] == self.left:
                self.section1 = [self.section0[1], self.right]
            elif self.section0[1] == self.right:
                self.section1 = [self.left, self.section0[0]]
            else:
                self.section1 = [[self.left, self.section0[0]], [self.section0[1], self.right]]
        if str(self.section0[0]).replace('.','',1).isdigit():
            self.result_teor += "\n\tПроміжок прияйняття нульової гіпотези: ( {0} ; {1} )".format(*self.section0)
        else:
            self.result_teor += "\n\tПроміжок прияйняття нульової гіпотези: ( {0} ; {1} )U( {2} ; {3} )".format(*self.section0[0],
                                                                                                    *self.section0[1])
        if str(self.section1[0]).replace('.', '', 1).isdigit():
            self.result_teor += "\n\tПроміжок прияйняття першої гіпотези: ( {0} ; {1} )".format(*self.section1)
        else:
            self.result_teor += "\n\tПроміжок прияйняття першої гіпотези: ( {0} ; {1} )U( {2} ; {3} )".format(*self.section1[0],
                                                                                                    *self.section1[1])

    def count_p1(self):
        if str(self.section1[0]).replace('.', '', 1).isdigit():
            self.p1 = self.n0.count_prob(self.section1[0], self.section1[1])
        else:
            self.p1 = self.n0.count_prob(self.section1[0][0], self.section1[0][1]) + \
                   self.n0.count_prob(self.section1[1][0], self.section1[1][1])

    def count_p2(self):
        if str(self.section0[0]).replace('.', '', 1).isdigit():
            self.p2 = self.s1.count_prob(self.section0[0], self.section0[1])
        else:
            self.p2 = self.s1.count_prob(self.section0[0][0], self.section0[0][1]) + \
                   self.s1.count_prob(self.section0[1][0], self.section0[1][1])

    def count_result_teor(self):
        if self.p1 != -1:
            self.find_y0_p1()
            self.make_sections()
            self.count_p2()
        elif self.p2 != -1:
            self.find_y0_p2()
            self.make_sections()
            self.count_p1()
        elif self.p != -1 and self.c1 !=-1 and self.c2 != -1:
            self.find_y0_pirson()
            self.make_sections()
            self.count_p1()
            self.count_p2()
        self.result_teor += "\n\tЙмовірність помилки першого роду: Р1 = {0}".format(self.p1)
        self.result_teor += "\n\tЙмовірність помилки другого роду: Р2 = {0}".format(self.p2)
        print(self.result_teor)

    def count_result_exp(self):
        counter = 0
        for i in range(1000):
            y = self.n0.generate()
            if str(self.section1[0]).replace('.', '', 1).isdigit():
                if self.section1[0] < y < self.section1[1]:
                    counter += 1
            else:
                if self.section1[0][0] < y < self.section1[0][1] or self.section1[1][0] < y < self.section1[1][1]:
                    counter += 1
        self.result_exp += "\n\tЙмовірність помилки першого роду: Р1 = {0}".format(counter/1000)
        counter = 0
        for i in range(1000):
            y = self.s1.generate()
            if str(self.section0[0]).replace('.', '', 1).isdigit():
                if self.section0[0] < y < self.section0[1]:
                    counter += 1
            else:
                if self.section0[0][0] < y < self.section0[0][1] or self.section0[1][0] < y < self.section0[1][1]:
                    counter += 1
        self.result_exp += "\n\tЙмовірність помилки другого роду: Р2 = {0}".format(counter / 1000)
        print(self.result_exp)


c = Counter(0, 1, 5, 3, p_a_not_b=0.2)
c.count_result_teor()
c.count_result_exp()

# c = Counter(10, 4, 5, 3, p_a_not_b=0.2)
# c.count_result_teor()
# c.count_result_exp()

# c2 = Counter(8, 1, 5, 2, p_b_not_a=0.96875)
# c2.count_result_teor()
# c2.count_result_exp()


# c3 = Counter(4, 2, 6, 3, p=0.5, c1=1, c2=1)
# c3.count_result_teor()
# c3.count_result_exp()
