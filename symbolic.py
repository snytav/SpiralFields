from sympy import *
from sympy.plotting import plot
x,n, p=var('x,n, p')

def besselj(p,x):
    return  summation(((-1)**n*x**(2*n+p))/(factorial(n)*gamma(n+p+1)*2**(2*n+p)),[n,0,oo])

def get_symbolic_field():
    k_numeric = 0.349  # cm^{-1}
    Bc_numeric = 0.5
    C_numeric = 30
    kc_numeric = k_numeric*C_numeric
    z_0_numeric = 0

    r, th, z, kc, z0, Bc = symbols('r th z kc z0 Bc')
    A_th_symbolic = -Bc / kc * cos(kc * (z - z0)) * besselj(1, kc * r)
    A_th_1 = A_th_symbolic.subs(kc, kc_numeric)
    A_th_2 = A_th_1.subs(Bc, Bc_numeric)
    A_th = A_th_2.subs(z0, z_0_numeric)
    print(A_th)
    qq = 0
    return A_th

def func_rz(expr,r_val,z_val):
    # from sympy import *
    r,z = symbols('r z')
    f = expr.subs(r,r_val).subs(z,z_val)
    return f.evalf()

if __name__ == '__main__':
    p1 = plot(besselj(0, x), (x, -20, 20), line_color='b', title=' $' + st + '$', show=False)
    p2 = plot(besselj(1, x), (x, -20, 20), line_color='g', show=False)
    p3 = plot(besselj(2, x), (x, -20, 20), line_color='r', show=False)
    p4 = plot(besselj(3, x), (x, -20, 20), line_color='c', show=False)
    p1.extend(p2)
    p1.extend(p3)
    p1.extend(p4)
    p1.show()
    qq = 0