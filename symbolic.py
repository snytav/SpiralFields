from sympy import *
from sympy.plotting import plot
# x,n, p=var('x,n, p')
from sympy.functions import besseli
#from spiral_field import kc,Bc
import numpy as np

B_0 = 100
beta = np.array([0, -0.575, 0, -0.000799, 0, -0.00000156])


def Atheta_2_sym():
    m = 1
    r,z,kc,z0,Bc = symbols('r z kc z0 Bc')
    Ath = -Bc/kc*besseli(m,kc*r)*sin(kc*(z-z0))
    return Ath

def Atheta_2_subs(r_n,z_n,z0_n,kc_num,Bc_num):
    r,z,kc,z0,Bc = symbols('r z kc z0 Bc')
    Ath = Atheta_2_sym()
    Ath_n = Ath.subs(r,r_n).subs(z,z_n).subs(z0,z0_n).subs(kc,kc_num).subs(Bc,Bc_num).evalf()
    return Ath_n

def Atheta_spiral_sym():
    #  Bc / kc * np.cos(kc * (zg_3d - z0)) * iv(0, kc * rg_3d)
    Bc,kc,z,r,z0,kc = symbols('Bc kc z r z0 kc')
    f = Bc*cos(kc*(z - z0))*besseli(0, kc*r)/kc
    return f

def Atheta_spiral_subs(Ath_sp,kcn,Bcn,r_n,z_n,z0_n):
    Bc, kc, z, r, z0, kc = symbols('Bc kc z r z0 kc')
    t = Ath_sp.subs(kc, kcn).subs(Bc, Bcn).subs(r, r_n).subs(z, z_n).subs(z0, z0_n).evalf()
    return t

def Atheta_1_sym():
    r,B0 = symbols('r B0')
    Ath = B0*r/2
    return Ath

def AthetaSum_sym():
    f = Atheta_1_sym()+Atheta_2_sym()
    return f

def Atheta_1_subs(B0_n,r_n,z_n,kc_n,z0_n,Bc_n):
    # r, B0 = symbols('r B0')
    r, z, kc, z0, Bc,B0 = symbols('r z kc z0 Bc B0')
    Ath = Atheta_1_sym()
    Ath_n = Ath.subs(r,r_n).subs(B0,B0_n).evalf()
    return Ath_n

def AthetaSum_subs(B0_n,r_n,z_n,z0_n,kc_n,Bc_num):
     t1 = Atheta_1_subs(B0_n,r_n,z_n,kc_n,z0_n,B0_n)
     t2 = Atheta_2_subs(z_n,z_n,z0_n,kc_n,Bc_num)
     t = t1+t2
     return t




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


def phi_spiral_sym():
    w,k,r = symbols('w k r')
    # f = w/k*r*Atheta_spiral_sym()
    f = w/k*r*(Atheta_1_sym()+Atheta_2_sym())
    return f

def phi_spiral_subs(kcn,Bcn,r_n,z_n,z0_n,w_n,k_n,B0_n):
    Bc, kc, z, r, z0, kc,k,w,B0 = symbols('Bc kc z r z0 kc k w B0')
    f = phi_spiral_sym()
    t = f.subs(kc, kcn).subs(Bc, Bcn).subs(r, r_n).subs(z,z_n).subs(z0,z0_n).subs(w,w_n).subs(k,k_n).subs(B0,B0_n).evalf()
    return t

def der_Atheta_r_sym():
    r = symbols('r')
    ath = AthetaSum_sym()
    f = diff(ath,r)
    return f

def der_Atheta_r_subs(kcn,Bcn,r_n,z_n,z0_n,w_n,k_n,B0_n):
    Bc, kc, z, r, z0, kc,k,w,B0 = symbols('Bc kc z r z0 kc k w B0')
    f = diff(der_Atheta_r_sym(),r)
    t = f.subs(kc, kcn).subs(Bc, Bcn).subs(r, r_n).subs(z,z_n).subs(z0,z0_n).subs(w,w_n).subs(k,k_n).subs(B0,B0_n).evalf()
    return t

def Er_spiral_sym():
    w, k, r = symbols('w k r')
    phi = phi_spiral_sym()
    f = diff(phi,r)
    return f

def Ez_spiral_sym():
    w, k, r,z = symbols('w k r z')
    phi = phi_spiral_sym()
    f = diff(phi,z)
    return f

def Er_spiral_subs(w_n, k_n, r_n, z_n,Bc_n,kc_n,z0_n,B0_n):
    w, k, r, z,Bc,kc,z0,B0 = symbols('w k r z Bc kc z0 B0')
    f = Er_spiral_sym()
    t = f.subs(r,r_n).subs(z,z_n).subs(Bc,Bc_n).subs(kc,kc_n).subs(z0,z0_n).subs(w,w_n).subs(k,k_n).subs(B0,B0_n)
    return t.evalf()


def Ez_spiral_subs(w_n, k_n, r_n, z_n,Bc_n,kc_n,z0_n):
    w, k, r, z,Bc,kc,z0 = symbols('w k r z Bc kc z0')
    f = Ez_spiral_sym()
    t = f.subs(r,r_n).subs(z,z_n).subs(Bc,Bc_n).subs(kc,kc_n).subs(z0,z0_n).subs(w,w_n).subs(k,k_n)
    return t.evalf()

def pps():
    Cm = 100*Array([0, -0.575, 0, -0.000799, 0, -0.00000156])
    m, th, k, z, r, i = symbols('m th k z r i')
    y = Cm[m] * sin(m * (th - k * z) * besseli(m, m * k * r))
    return y

def pps_subs(th_n,r_n,z_n,k_n,m_n):
    m, th, k, z, r, i = symbols('m th k z r i')
    f = phi_s()
    t = f.subs(m,m_n).subs(th,th_n).subs(k,k_n).subs(z,z_n).subs(r,r_n).evalf()
    return t



def phi_s():
    Cm = Array([0, -0.575e2, 0, -0.000799e2, 0, -0.00000156e2])
    m, th, k, z, r, i = symbols('m th k z r i')
    y = Sum(Cm[m] * sin(m * (th - k * z) * besseli(m, m * k * r)), (m, 1, 5))
    return y

def phi_s_subs(th_n,r_n,z_n,k_n):
    m, th, k, z, r, i = symbols('m th k z r i')
    f = phi_s()
    t = f.subs(th,th_n).subs(k,k_n).subs(z,z_n).subs(r,r_n).evalf()
    return t

def d_phi_s_d_r():
    f = phi_s()
    r = symbols('r')
    y = diff(f,r)
    return y

def d_phi_s_d_th():
    f = phi_s()
    th = symbols('th')
    y = diff(f,th)
    return y

def d_phi_s_d_z():
    f = phi_s()
    z = symbols('z')
    y = diff(f,z)
    return y

def d_phi_s_subs(f,th_n,r_n,z_n,k_n):
    m, th, k, z, r, i = symbols('m th k z r i')
    t = f.subs(th,th_n).subs(k,k_n).subs(z,z_n).subs(r,r_n).evalf()
    return t



if __name__ == '__main__':

    # #p1 = plot(besselj(0, x), (x, -20, 20), line_color='b', title=' $' + st + '$', show=False)
    # p2 = plot(besselj(1, x), (x, -20, 20), line_color='g', show=False)
    # p3 = plot(besselj(2, x), (x, -20, 20), line_color='r', show=False)
    # p4 = plot(besselj(3, x), (x, -20, 20), line_color='c', show=False)
    # p1.extend(p2)
    # p1.extend(p3)
    # p1.extend(p4)
    # p1.show()
    qq = 0