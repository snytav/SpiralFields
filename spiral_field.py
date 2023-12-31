import numpy as np
#TODO^ make Atheta_Sum_subs(), verufy AthetaSum
#TODO and the following expression for phi_spiral
from matplotlib.animation import ArtistAnimation

import matplotlib

from matplotlib import pyplot as plt
from scipy.special import iv, ivp

# Константы
B_0 = 100
Bc = 0.5
C = 30
z0 = 0
k = 0.349
kc = C * k
beta = np.array([0, -0.575, 0, -0.000799, 0, -0.00000156])
Cm = B_0 * beta
w = 1000000
tau = 0.001
e = 1
c = 1
m = 1

# Сетка 3D
r_linspace = np.linspace(0, 1, 50)
z_linspace = np.linspace(0, 1, 50)
theta_linspace = np.linspace(0, 2 * np.pi, 60)
thetag_3d, rg_3d, zg_3d = np.meshgrid(theta_linspace, r_linspace, z_linspace)
X_3d, Y_3d, Z_3d = rg_3d * np.cos(thetag_3d), rg_3d * np.sin(thetag_3d), zg_3d

# Сетка 2D (поперечный срез)
tg_2dp, rg_2dp = np.meshgrid(theta_linspace, r_linspace)

# Сетка 2D (продольный срез)
zg_2d, rg_2d = np.meshgrid(z_linspace, r_linspace)


def draw_3d(values, title='Untitled', vmin=None, vmax=None, ax_3d=None, save=None):
    if ax_3d is None:
        fig = plt.figure(figsize=(10, 9))
        ax_3d = fig.add_subplot(projection='3d')

    # Меняем местами x и z, чтобы цилиндр лежал на боку
    p = ax_3d.scatter(Z_3d, Y_3d, X_3d, c=values, s=10, cmap='plasma')  # norm=matplotlib.colors.LogNorm()
    # ax_3d.set_title(title, fontsize=14)
    ax_3d.set_xlabel('z', fontsize=14)

    if save is not None:
        plt.savefig(save + '.png')

    return p


def draw_circle_slice(values, at_z, title='Untitled', colorbar_title='Variable', vmin=None, vmax=None, save=None):
    closest_index = -1
    closest_diff = 9999999
    closest_z = -1

    for i in range(len(z_linspace)):
        z = z_linspace[i]
        diff = np.abs(z - at_z)
        if diff < closest_diff:
            closest_diff = diff
            closest_index = i
            closest_z = z

    closest_z = round(closest_z, 4)

    fig = plt.figure(figsize=(6, 7))
    ax = fig.add_subplot(polar=True)
    plt.grid(False)
    # ax.set_title('Поперечный срез цилиндра\n' + title + f'\nz = {closest_z}')
    p = ax.pcolor(tg_2dp, rg_2dp, values[:, :, closest_index], cmap='plasma', vmin=vmin, vmax=vmax)
    cb = fig.colorbar(p, ax=ax)
    # cb.set_label(colorbar_title, fontsize=14)

    if save is not None:
        plt.savefig(save + '.png')

    return p


def draw_rectangle_slice(values, title='Untitled', colorbar_title='Variable', vmin=None, vmax=None, save=None):
    fig, ax = plt.subplots(figsize=(6, 7))
    p = ax.pcolor(zg_2d, rg_2d, values[:, 0, :], cmap='plasma', vmin=vmin, vmax=vmax)

    # ax.set_title('Продольный срез цилиндра\n' + title, fontsize=14)
    ax.set_xlabel('z', fontsize=14)
    ax.set_ylabel('r', fontsize=14)

    cb = fig.colorbar(p, ax=ax)
    cb.set_label(colorbar_title, fontsize=14)

    if save is not None:
        plt.savefig(save + '.png')

    return p


def compute_B(derivative_fc_r, derivative_fc_theta, derivative_fc_z, derivative_fs_r, derivative_fs_theta,
              derivative_fs_z):
    Br = derivative_fs_r + derivative_fc_r
    Btheta = derivative_fs_theta + derivative_fc_theta
    Bz = B_0 + derivative_fs_z + derivative_fc_z

    return Br, Btheta, Bz


def compute_V(Er, Etheta, Ez, Br, Btheta, Bz):
    Vtheta = np.zeros((50, 60, 50))
    Vz = np.zeros((50, 60, 50))
    Vr = np.zeros((50, 60, 50))

    # Vz[:,:,0] = 1

    timesteps = 5

    Vr_last = Vr
    Vtheta_last = Vtheta
    Vz_last = Vz

    for i in range(timesteps):
        Vr = Vr_last + tau * e / (m * c) * (Vtheta_last * Bz - Vz_last * Btheta) + tau * e / m * Er
        Vtheta = Vtheta_last + tau * e / (m * c) * (-Vr_last * Bz + Vz_last * Br) + tau * e / m * Etheta
        Vz = Vz_last + tau * e / (m * c) * (-Vr_last * Btheta + Vtheta_last * Br) + tau * e / m * Ez

        Vr_last = Vr
        Vtheta_last = Vtheta
        Vz_last = Vz

    return Vr_last, Vtheta_last, Vz_last


def get_spiral_fields():
    zeros = np.zeros((50, 60, 50))

    plt.rcParams.update({'figure.max_open_warning': 0})

    fc = Bc / kc * np.cos(kc * (zg_3d - z0)) * iv(0, kc * rg_3d)
    from symbolic import Atheta_spiral_sym,Atheta_spiral_subs
    Ath_sp = Atheta_spiral_sym()
    ath_num = Atheta_spiral_subs(Ath_sp,kc,Bc,r_linspace[1],z_linspace[1],z0)
    fs = np.zeros((50, 60, 50))

    from symbolic import pps,pps_subs
    for m in range(1, 6):
        fs += Cm[m] * np.sin(m * (thetag_3d - k * zg_3d)) * iv(m, m * k * rg_3d)
        t_n = Cm[m] * np.sin(m * (thetag_3d - k * zg_3d)) * iv(m, m * k * rg_3d)
        t = pps_subs(theta_linspace[1],r_linspace[1],z_linspace[1],k,m)
        dt = t-t_n[1][1][1]
        qq = 0

    from symbolic import phi_s,phi_s_subs
    f = phi_s_subs(theta_linspace[1],r_linspace[1],z_linspace[1],k)
    qq = 0

    derivative_fs_r = 0.0
    for m in range(1, 6):
        multiplier1 = Cm[m] * np.sin(m * (thetag_3d - k * zg_3d))
        multiplier2 = 0.0

        for i in range(10):
            denom = np.math.factorial(i) * np.math.factorial(i + m)
            multiplier2 += ((m * k / 2) ** (2 * i + m)) * (2 * i + m) * (rg_3d ** (2 * i + m - 1)) / denom

        derivative_fs_r += multiplier1 * multiplier2

    from symbolic import d_phi_s_d_r,d_phi_s_subs
    fs_r111_t = d_phi_s_subs(d_phi_s_d_r(),theta_linspace[1],r_linspace[1],z_linspace[1],k)
    fs_r111_n = derivative_fs_r[1][1][1]
    d111 = fs_r111_n-fs_r111_t

    derivative_fs_theta = 0.0
    for m in range(1, 6):
        derivative_fs_theta = derivative_fs_theta + Cm[m] * np.cos(m * (thetag_3d - k * zg_3d)) * m * iv(m,

                                                                                                         m * k * rg_3d)
    from symbolic import d_phi_s_d_th
    fs_th111_t = d_phi_s_subs(d_phi_s_d_th(), theta_linspace[1], r_linspace[1], z_linspace[1], k)
    fs_th111_n = derivative_fs_theta[1][1][1]
    d111th = fs_th111_n - fs_th111_t

    derivative_fs_z = 0.0
    for m in range(1, 6):
        derivative_fs_z = derivative_fs_z - Cm[m] * m * k * np.cos(m * (thetag_3d - k * zg_3d)) * iv(m, m * k * rg_3d)

    from symbolic import d_phi_s_d_th,d_phi_s_d_z
    fs_z111_t = d_phi_s_subs(d_phi_s_d_z(), theta_linspace[1], r_linspace[1], z_linspace[1], k)
    fs_z111_n = derivative_fs_z[1][1][1]
    d111z = fs_z111_n - fs_z111_t

    derivative_fc_r = 0.0
    multiplier = 0.0
    for i in range(1, 11):
        v = (kc / 2) ** (2 * i) * 2 * i * rg_3d ** (2 * i - 1) / np.math.factorial(i) ** 2
        multiplier += v

    derivative_fc_r = Bc / kc * np.cos(kc * (zg_3d - z0)) * multiplier

    derivative_fc_theta = 0.0

    derivative_fc_z = 0.0
    for m in range(10):
        derivative_fc_z = derivative_fc_z - Bc * np.sin(kc * (zg_3d - z0)) * iv(0, kc * rg_3d)

    Ar = 0.0
    for m in range(1, 6):
        v1 = Cm[m]
        v2 = np.sin(m * (thetag_3d - k * zg_3d))
        v3 = k * rg_3d * iv(m, m * k * rg_3d)
        Ar = Ar + v1 * v2 * v3

    Az = 0.0
    for m in range(1, 6):
        v1 = Cm[m]
        v2 = np.cos(m * (thetag_3d - k * zg_3d))
        v3 = k * rg_3d * ivp(m, m * k * rg_3d)
        Az = Az + v1 * v2 * v3
    Az = -Az

    Atheta_1 = B_0 * rg_3d / 2
    from symbolic import Atheta_2_sym,Atheta_2_subs,Atheta_1_sym,Atheta_1_subs

    v1 = -Bc / kc
    v2 = np.sin(kc * (zg_3d - z0))
    v3 = iv(1, kc * rg_3d)

    Atheta_2 = v1 * v2 * v3

    AthetaSum = Atheta_1 + Atheta_2

    at1_num = Atheta_1[1][1][1]
    at2_num = Atheta_2[1][1][1]
    at2 = Atheta_2_subs(r_linspace[1], z_linspace[1], 0.0, kc, Bc)
    at1 = Atheta_1_subs(B_0,r_linspace[1],z_linspace[1],kc,z0,Bc)
    dt1 = at1-at1_num
    dt2 = at2 - at2_num
    from symbolic import AthetaSum_subs,AthetaSum_sym
    aths    = AthetaSum_subs(B_0,r_linspace[1],z_linspace[1],z0,kc,Bc)
    aths_num = AthetaSum[1][1][1]
    dts = aths - aths_num


    ### Er
    derivative_Atheta_r = 0.0
    multiplier = 0.0
    for j in range(10):
        multiplier = multiplier + (kc / 2) ** (2 * j + 1) * (2 * j + 1) * rg_3d ** (2 * j) / (
                    np.math.factorial(j) * np.math.factorial(j + 1))
    derivative_Atheta_r = B_0 / 2 - Bc / kc * np.sin(kc * (zg_3d - z0)) * multiplier

    derivative_Az_r = 0.0
    for m in range(1, 6):
        multiplier = 0.0
        for i in range(10):
            denom = (np.math.factorial(i) * np.math.factorial(i + m))
            multiplier += ((2 * i + m) ** 2) / denom * (0.5 ** (2 * i + m)) * ((m * k * rg_3d) ** (2 * i + m - 1))
        derivative_Az_r = derivative_Az_r - Cm[m] * np.cos(m * (thetag_3d - k * zg_3d)) * k * multiplier

    ### Etheta
    derivative_Az_theta = 0.0
    for m in range(1, 6):
        derivative_Az_theta = derivative_Az_theta + Cm[m] * k * rg_3d * ivp(m, m * k * rg_3d) * np.sin(
            m * (thetag_3d - k * zg_3d)) * m

    ### Ez
    derivative_Az_z = 0.0
    for m in range(1, 6):
        derivative_Az_z = derivative_Az_z - Cm[m] * np.sin(m * (thetag_3d - k * zg_3d)) * m * k ** 2 * rg_3d * ivp(m,
                                                                                                                   m * k * rg_3d)
    derivative_Atheta_z = -Bc * np.cos(kc * (zg_3d - z0)) * iv(1, kc * rg_3d)

    phi_corrugation = w / k * (rg_3d * B_0 * rg_3d / 2 + Az / k)
    phi_spiral = w / k * (rg_3d * AthetaSum)
    phi_full = w / k * (rg_3d * AthetaSum + Az / k)

    from symbolic import phi_spiral_sym,phi_spiral_subs
    phi_ss = phi_spiral_sym()
    p11 = phi_spiral_subs(kc,Bc,r_linspace[1],z_linspace[1],z0,w,k,B_0)
    p11_num= phi_spiral[1][1][1]
    dp = np.abs(p11 - p11_num)/p11

    # Er_full     = w / k * (AthetaSum + rg_3d * derivative_Atheta_r + 1 / k * derivative_Az_r)
    # Etheta_full = w / (k ** 2) * derivative_Az_theta
    # Ez_full     = w / k * (rg_3d * derivative_Atheta_z + 1 / k * derivative_Az_z)

    # Er_corrugation     = w / k * (B_0 * rg_3d + 1 / k * derivative_Az_r)
    # Etheta_corrugation = w / (k ** 2) * derivative_Az_theta
    # Ez_corrugation     = w / (k ** 2) * derivative_Az_z

    Er_spiral = w / k * (AthetaSum + rg_3d * derivative_Atheta_r) # NOT EXACTLY MATHING ANALYTICAL VALUES
    from symbolic import der_Atheta_r_sym,der_Atheta_r_subs
    dath = der_Atheta_r_subs(kc,Bc,r_linspace[1],z_linspace[1],z0,w,k,B_0)
    dath_num = derivative_Atheta_r[1][1][1]
    d_ath_r = dath-dath_num
    # Here Atheta - analytical is just Atheta_1, and in numerical we see AthetaSum !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    from symbolic import Er_spiral_sym,Atheta_spiral_sym
    Er_ss = Er_spiral_sym()

    Etheta_spiral = np.zeros((50, 60, 50))
    Ez_spiral = w / k * rg_3d * derivative_Atheta_z
    from symbolic import  Ez_spiral_sym,Ez_spiral_subs,Er_spiral_subs
    Ez_ss = Ez_spiral_sym()
    ezt = Ez_spiral_subs(w,k,r_linspace[1],z_linspace[1],Bc,kc,z0)-Ez_spiral[1][1][1]
    ert = Er_spiral_subs(w, k, r_linspace[1], z_linspace[1], Bc, kc, z0,B_0)-Er_spiral[1][1][1]

    Br_spiral, Btheta_spiral, Bz_spiral = compute_B(zeros, zeros, zeros, derivative_fs_r, derivative_fs_theta,
                                                    derivative_fs_z)

    # Br_corrugation, Btheta_corrugation, Bz_corrugation = compute_B(derivative_fc_r, derivative_fc_theta, derivative_fc_z, zeros, zeros, zeros)
    # Br_full, Btheta_full, Bz_full = compute_B(derivative_fc_r, derivative_fc_theta, derivative_fc_z, derivative_fs_r, derivative_fs_theta, derivative_fs_z)

    Vr_spiral, Vtheta_spiral, Vz_spiral = compute_V(Er_spiral, Etheta_spiral, Ez_spiral, Br_spiral, Btheta_spiral,
                                                    Bz_spiral)
    # Vr_corrugation, Vtheta_corrugation, Vz_corrugation = compute_V(Er_corrugation, Etheta_corrugation, Ez_corrugation, Br_corrugation, Btheta_corrugation, Bz_corrugation)
    # Vr_full, Vtheta_full, Vz_full = compute_V(Er_full, Etheta_full, Ez_full, Br_full, Btheta_full, Bz_full)

    component_title = ['r', 'theta', 'z']

    # Отрисовка E
    for i, E in enumerate([Er_spiral, Etheta_spiral, Ez_spiral]):
        title = component_title[i]
        bmin = E.min()
        bmax = E.max()
        #draw_3d(E, vmin=bmin, vmax=bmax, title="E" + title + "spiral")
        #draw_rectangle_slice(E, vmin=bmin, vmax=bmax, title="E" + title + "spiral")
        #draw_circle_slice(E, 0.5, vmin=bmin, vmax=bmax)

    # Отрисовка B
    for i, B in enumerate([Br_spiral, Btheta_spiral, Bz_spiral]):
        title = component_title[i]
        bmin = B.min()
        bmax = B.max()
        #draw_3d(B, vmin=bmin, vmax=bmax, save='B' + title + '_spiral_3d' + '_' + str(C))
        #draw_rectangle_slice(B, vmin=bmin, vmax=bmax, save='B' + title + '_spiral_rect' + '_' + str(C))
        #draw_circle_slice(B, 0.5, vmin=bmin, vmax=bmax, save='B' + title + '_spiral_circle' + '_' + str(C))

    # Отрисовка V
    for i, V in enumerate([Vr_spiral, Vtheta_spiral, Vz_spiral]):
        title = component_title[i]
        vmin = V.min()
        vmax = V.max()
        #draw_3d(V, vmin=vmin, vmax=vmax, save='V' + title + '_spiral_3d' + '_' + str(C))
        #draw_rectangle_slice(V, vmin=vmin, vmax=vmax, save='V' + title + '_spiral_rect' + '_' + str(C))
        #draw_circle_slice(V, 0.5, vmin=vmin, vmax=vmax, save='V' + title + '_spiral_circle' + '_' + str(C))

    return Atheta_1,Atheta_2,AthetaSum,Er_spiral,Etheta_spiral,Ez_spiral,Br_spiral,Btheta_spiral,Bz_spiral,r_linspace, theta_linspace, z_linspace

class CylindricalField:
    def __init__(self):
        Ath1,Ath2,Ath,Er, Eth, Ez, Br, Bth, Bz, r_linspace, theta_linspace, z_linspace = get_spiral_fields()
        self.Er  = Er
        self.Eth = Eth
        self.Ez  = Ez
        self.Br  = Br
        self.Bth = Bth
        self.Bz  = Bz
        self.r_linspace     = r_linspace
        self.theta_linspace = theta_linspace
        self.z_linspace     = z_linspace
        self.x0 = np.zeros(3)
        self.Ath1 = Ath1
        self.Ath2 = Ath2
        self.Ath = Ath

    def getR(self):
        return self.r_linspace[-1]

    def get_grid_step(self):
        h_r  = self.r_linspace[1]     - self.r_linspace[0]
        h_th = self.theta_linspace[1] - self.theta_linspace[0]
        h_z = self.z_linspace[1]      - self.z_linspace[0]
        return np.array([h_r,h_th,h_z])



    def get_field(self,r,th,z):
        from push_cylindrical import get_polar_field_2D, XtoL
        xcyl = np.array([r, th, z])
        dh = self.get_grid_step()
        lc = XtoL(xcyl, self.x0, dh)
        dr = dh[0]


        er = get_polar_field_2D(lc, r, dr, self.Er)
        et = get_polar_field_2D(lc, r, dr, self.Eth)
        ez = get_polar_field_2D(lc, r, dr, self.Ez)
        br = get_polar_field_2D(lc, r, dr, self.Br)
        bt = get_polar_field_2D(lc, r, dr, self.Bth)
        bz = get_polar_field_2D(lc, r, dr, self.Bz)
        at = get_polar_field_2D(lc, r, dr, self.Ath)
        return er,et,ez,br,bt,bz,at
    def draw_fields(self):
        from cyl_plot import draw_cylidrical_field
        draw_cylidrical_field(self.Er, self.r_linspace, self.theta_linspace, self.z_linspace, "Er")
        draw_cylidrical_field(self.Br, self.r_linspace, self.theta_linspace, self.z_linspace, "Br")

        draw_cylidrical_field(self.Eth, self.r_linspace, self.theta_linspace, self.z_linspace, "Eth")
        draw_cylidrical_field(self.Bth, self.r_linspace, self.theta_linspace, self.z_linspace, "Bth")

        draw_cylidrical_field(self.Ez, self.r_linspace, self.theta_linspace, self.z_linspace, "Ez")
        draw_cylidrical_field(self.Bz, self.r_linspace, self.theta_linspace, self.z_linspace, "Bz")


if __name__ == '__main__':
     cf = CylindricalField()
     er,et,ez,br,bt,bz = cf.get_field(0.1,0.1,0.1)
     cf.draw_fields()




