from sympy import *
from sympy.plotting import plot
x,n, p=var('x,n, p')

def besselj(p,x):
    return  summation(((-1)**n*x**(2*n+p))/(factorial(n)*gamma(n+p+1)*2**(2*n+p)),[n,0,oo])

def get_symbolic_field():
    k_numeric = 0.349  # cm^{-1}
    Bc_numeric = 0.5
    C_numeric = 1
    z_0_numeric = 0

    r, th, z, kc, z0, Bc = symbols('r th z kc z0 Bc')
    A_th_symbolic = -Bc / kc * cos(kc * (z - z0)) * besselj(1, kc * r)
    A_th_1 = A_th_symbolic.subs(kc, k_numeric)
    A_th_2 = A_th_1.subs(Bc, Bc_numeric)
    A_th = A_th_2.subs(z0, z_0_numeric)
    print(A_th)
    qq = 0
    return A_th