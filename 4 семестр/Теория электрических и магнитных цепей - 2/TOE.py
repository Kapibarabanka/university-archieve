import cmath
import math
ua = cmath.rect(200, math.radians(-20))
ub = cmath.rect(200, math.radians(-140))
uc = cmath.rect(200, math.radians(100))
r = 56
xlin = 7
xl = 33
xc = 84

zab1 = (r+xl*1j)*(r-xc*1j)/(2*r+xl*1j-xc*1j)
za = zab1/3+xlin*1j
ia = ua/za
ib = ub/za
ic = uc/za

uab = ua - ub
ubc = ub - uc
uca = uc - ua

u1ab = uab - ia*xlin*1j + ib*xlin*1j
u1bc = ubc - ib*xlin*1j + ic*xlin*1j
u1ca = uca - ic*xlin*1j + ia*xlin*1j

i2ab = u1ab/(r-xc*1j)
i2bc = u1bc/(r-xc*1j)
i2ca = u1ca/(r-xc*1j)

i1ab = u1ab/(r+xl*1j)
i1bc = u1bc/(r+xl*1j)
i1ca = u1ca/(r+xl*1j)

i2a = i2ab - i2ca
i2b = i2bc - i2ab
i2c = i2ca - i2bc

i1a = ia - i2a
i1b = ib - i2b
i1c = ic - i2c

print(i2ab*7, cmath.polar(i2ab*7))
print((ia.real-ia.imag*1j)*(ua-uc))
# s = ua*(ia.real-ia.imag*1j)+ub*(ib.real-ib.imag*1j)+uc*(ic.real-ic.imag*1j)
# p = 3*r*(abs(i2ab)**2+abs(i1ab)**2)
# q = 3*(abs(ia)**2*xlin-abs(i2ab)**2*xc+abs(i1ab)**2*xl)
# print(i1a,i1b,i1c)
# print(abs(i1a),abs(i1b),abs(i1c))
# print(math.degrees(cmath.phase(i1a)),math.degrees(cmath.phase(i1b)),math.degrees(cmath.phase(i1c)))
# print("s =", s)
# print("p =", p)
# print("q =", q)


