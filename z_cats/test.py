from visualise import box
from load_data import load_snap
import h5py as h
import matplotlib.pyplot as plt
import numpy as np

pth = '/home/acer/arepo_runs/cosmo_box_star_formation_3d/output'

for a in range(20):
    file = pth + f'/snap_{a:03d}.hdf5'
    #plotting snaps 
    fig, ax = plt.subplots(figsize = (20, 20), subplot_kw = {'projection': '3d'}, facecolor = 'black')
    coord = h.File(file, 'r')['PartType0']['Coordinates'][:]
    coord1 = h.File(file, 'r')['PartType1']['Coordinates'][:]
    coord4 = h.File(file, 'r')['PartType1']['Coordinates'][:]

    x = []
    for i in coord[:, 0]:
        x.append(i)
    for j in coord1[:, 0]:
            x.append(j)
    for k in coord4[:, 0]:
            x.append(k)
    x = np.array(x)

    y = []
    for l in coord[:, 1]:
        y.append(l)
    for m in coord1[:, 1]:
            y.append(m)
    for n in coord4[:, 1]:
            y.append(n)
    y = np.array(y)


    z = []
    for o in coord[:, 2]:
        z.append(o)
    for p in coord1[:, 2]:
            z.append(p)
    for q in coord4[:, 2]:
            z.append(q)
    z = np.array(z)

    #print(coord[:10])

    ax.scatter(x/1e3, y/1e3, z/1e3, s = 0.0001, alpha = 1,  color = 'white')

    ax.set_facecolor('black')
    ax.set_aspect('equal')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.set_xlabel('x(Mpc)', fontsize = 12)
    ax.set_ylabel('y(Mpc)', fontsize = 12)
    ax.set_zlabel('z(Mpc)', fontsize = 12)

    #ax.set_xlim(40, 60)
    #ax.set_ylim(40, 60)
    #ax.set_zlim(40, 60)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.zaxis.label.set_color('white')

    ax.tick_params(colors = 'white')

    ax.grid(False)
    plt.savefig(f'./snap_imgs/snap_{a:03d}.png')
    plt.close(fig)

