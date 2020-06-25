import math
import random


class Counter:
    correlation_t = 3/19

    def __init__(self, a=3, b=1, step=0.001, n=10):
        self.a = a
        self.b = b
        self.h = 3/a/b
        self.step = step
        self.n = n

    def phi_x(self, x):
        return 3*(self.a**2-x**2)/(2*self.a**3)

    def cond_y(self, x0, cur_y):
        if cur_y >= 0 and cur_y <= self.b*x0/self.a:
            return 2 * self.a / self.b / (self.a *self.a - x0*x0) * (self.a - x0)
        if cur_y > self.b*x0/self.a and cur_y <= self.b:
            return 2 * self.a*self.a / self.b / (self.a *self.a - x0*x0) * (self.b - cur_y) / self.b

    def count_x(self, r):
        square = 0
        cur_x = 0
        while square < r:
            cur_x += self.step
            square += math.fabs(self.phi_x(cur_x)+self.phi_x(cur_x-self.step))/2 * self.step
        return cur_x

    def count_y(self, r, x):
        square = 0
        cur_y = 0
        while square < r:
            cur_y += self.step
            square += math.fabs(self.cond_y(x, cur_y)+self.cond_y(x,cur_y-self.step))/2 * self.step
        return cur_y

    def generate(self):
        for i in range(self.n):
           r = random.random()
           self.x_exp.append(self.count_x(r))
           r = random.random()
           self.y_exp.append(self.count_y(r, self.x_exp[i]))

    def count_m(self):
        self.m_x = sum(self.x_exp) / self.n
        self.m_y = sum(self.y_exp) / self.n

    def count_sigm(self):
        self.sigma_x = math.sqrt(sum(map(lambda x: x*x, self.x_exp)) / self.n - self.m_x*self.m_x)
        self.sigma_y = math.sqrt(sum(map(lambda x: x*x, self.y_exp)) / self.n - self.m_y*self.m_y)

    def count_cov(self):
        self.cov = sum(map(lambda tup: tup[0]*tup[1], zip(self.x_exp, self.y_exp))) / self.n - self.m_x*self.m_y

    def count_cor(self):
        self.count_cov()
        self.correlation = self.cov/self.sigma_x/self.sigma_y

    def count_theory(self):
        self.m_x_t = 3*self.a/8
        self.m_y_t = 3 * self.b / 8
        self.sigma_x_t = self.a / 40 * math.sqrt(95)
        self.sigma_y_t = self.b / 40 * math.sqrt(95)
        self.cov_t = 3*self.a*self.b/320


    def do_lab(self):
        print("Counting...")
        self.x_exp = []
        self.y_exp = []
        self.generate()
        self.count_m()
        self.count_sigm()
        self.count_cor()
        self.count_theory()
        count = 0
        for i in range(len(self.x_exp)):
            if self.x_exp[i] > 0.5:
                count += 1
        print(count/len(self.x_exp))



