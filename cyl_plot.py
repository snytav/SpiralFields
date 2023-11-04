import matplotlib.pyplot as plt
import numpy as np
from push_cylindrical import pol2cart
from draw_cylinder import draw_cyl_3D_along_Z

def draw_particle_3D(x,y,z,clr,ax):

    ax.scatter(x, y, z,  color=clr)
    # draw_cyl_3D_along_Z(center_x, center_y, radius, height_z, ax)

    qq = 0




def multi_particles_3D(x,name):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.set_xlim(np.min(x[:,:,0]), np.max(x[:,:,0]))
    ax.set_ylim(np.min(x[:,:,1]), np.max(x[:,:,1]))
    ax.set_zlim(np.min(x[:,:,2]), np.max(x[:,:,2]))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    x1 = np.min(x[:,:,0])+np.max(x[:,:,0])/2
    y1 = np.min(x[:, :, 1]) + np.max(x[:, :, 1]) / 2
    z0 = np.min(x[:,:,2])
    z1 = np.max(x[:, :, 2])
    # ax.quiver(x1, x1, y1,y1,z0,z1, length=1.5*(z1-z0), normalize=True)


    colors = ['red', 'blue', 'brown', 'green', 'yellow', 'magenta', 'grey', 'cyan', 'black']

    for n in range(x.shape[0]):
        xdata = x[n,:,0]
        ydata = x[n,:,1]
        zz    = x[n,:,2]
        c     = colors[n%len(colors)]
        draw_particle_3D(xdata, ydata, zz, c, ax)
        qq = 0

    #ax.plot(xdata, ydata, zz,  color=clr)
    # draw_cyl_3D_along_Z(0.0, 0.0, 1.0, 1.0, ax)
    plt.savefig(name+'.png')

    qq = 0
#
def draw_cylidric_particles(rr,theta,zz,center_x, center_y, radius, height_z,clr,fig,ax):

    xdata = []
    ydata = []
    for r,th in zip(rr,theta):
        x, y = pol2cart(r, th)
        xdata.append(x)
        ydata.append(y)

    xdata = np.array(xdata)
    ydata = np.array(ydata)
    ax.scatter3D(xdata, ydata, zz, color=clr);
    draw_cyl_3D_along_Z(center_x, center_y, radius, height_z, ax)

    qq = 0

from push_cylindrical import XtoL,get_polar_field_2D,get_theta

def cylidrical_2_cartesion(fc,r_linspace,theta_linspace,z_linspace):
    rm = np.max(r_linspace)
    dr = r_linspace[1] - r_linspace[0]
    dtheta = theta_linspace[1] - theta_linspace[0]
    dz = z_linspace[1] - z_linspace[0]
    dh = np.array([dr, dtheta, dz])
    x0 = np.zeros(3)

    nr,nt,nz = fc.shape
    f = np.zeros((2*nr,2*nr,nz))
    for ix in range(2*nr):
        for iy in range(2*nr):
            for iz in range(nz-1):
                x = ix*dr - rm
                y = iy*dr - rm
                z = iz*dz
                r  = np.power(x*x+y*y,0.5)
                if r < rm:
                    th = get_theta(x,y)
                    xcyl = np.array([r, th, z])
                    lc = XtoL(xcyl, x0, dh)

                    er = get_polar_field_2D(lc, r, dr, fc)
                    f[ix][iy][iz]= er
    return f

from field3D import volume_field_plot

def draw_cylidrical_field(fc, r_linspace, theta_linspace, z_linspace,name):
    f = cylidrical_2_cartesion(fc, r_linspace, theta_linspace, z_linspace)
    volume_field_plot(f,name)
