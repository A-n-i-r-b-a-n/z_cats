import numpy as np
import matplotlib.pyplot as plt
import h5py as h
from PIL import Image
from pathlib import Path
import pyvista as pv
from . import load_data


##############################################################################
# Making a movie (.gif files from snaps)
##############################################################################

def movie(path, **kwargs):
    """
    Takes the path and other parameters to create a gif from multiple .png fr-
    ames

    path: string type; takes the path of the folder where the .png snaps exist

    duration: integer type; determines the duration per frame of the final .g-
    if file, uses 1000 ms as default value if no argument is given.

    loop: integer type; determines the number of times the .gif file should l-
    oop, uses 0 as default if no argument is given.

    out_path: string type; determines the output folder where the .gif file wo-
    uld be saved, uses current directory as default if no argument is given.
    
    output: string type; detrermines the name of the final output file, uses t-
    he name output as default if no argument is given.
    """
    files = sorted(
        Path(path).glob('snap_*.png'),
        key=lambda f: int(f.stem.split('_')[1])
    )

    frames = [Image.open(f) for f in files]


    #manage the duration per frame
    if ('duration' in kwargs.keys()):
        t = kwargs['duration']
    else:
        t = 1000
    
    #manage the output path
    if ('out_path' in  kwargs.keys()):
        out = kwargs['out_path']
    else:
        out = '.'
    
    #manage the name of the generated gif
    if ('output' in kwargs.keys()):
        nm = kwargs['output']
    else:
        nm = 'output.gif'
    
    #manage the number of times the gif loops
    if ('loop' in kwargs.keys()):
        l = kwargs['loop']
    else:
        l = 0
    
    #saving the gif
    frames[0].save(
            f'{out}/{nm}',
            save_all = True, 
            append_images = frames[1:],
            duration = t,
            loop = l
            )

    return None
#------------------------------------------------------------------------------#

################################################################################
# Plotting 3D box
################################################################################

def box(label, *data, **kwargs):
    """
    Takes data and other parameters to create a 3D interactable
    box 

    label: list type containing string type x label, y lablel and 
    z label

    data: array type, containing the data for generating the poin-
    tcloud 

    point_size: type, double, determines the point size of the poi-
    nt size

    font_size: type, integer, determines the font size of the label

    rotate: type, boolean, determines whether the box rotates while 
    displaying

    """
    plotter = pv.Plotter()
    window_size = (1920, 1080)
    #set point size
    if 'point_size' in kwargs.keys():
        p = kwargs['point_size']
    else:
        p = 1

    #set font size
    if 'font_size' in kwargs.keys():
        f = kwargs['font_size']
    else:
        f = 10

    if 'rotate' in kwargs.keys():
        r = kwargs['rotate']
    else:
        r = False
    
    #datasets
    for i in data:
        cloud = pv.PolyData(i)
        plotter.add_points(cloud, point_size = p)

    #final plot operation
    
    plotter.show_bounds(
    location='outer',
    xtitle= label[0],
    ytitle= label[1],
    ztitle= label[2],

    color = 'white',
    font_size = f,
    n_xlabels = 5,
    n_ylabels = 5,
    n_zlabels = 5 )

    plotter.add_axes()
    plotter.set_background('black')

    if r:
        plotter.view_xz()
        plotter.show(auto_close = False)
        plotter.open_gif('rotation.gif')

        for i in range(180):
            plotter.camera.azimuth += 1
            plotter.render()
            plotter.write_frame()
        plotter.close()

    else:
        plotter.show()

    return None
#-------------------------------------------------------------------------------#

################################################################################
# generating png files from a snap
################################################################################

def create_image(snap, **kwargs):

    if "PartType" in kwargs.keys():
        pt = kwargs['PartType']
    else:
        pt = 1

    if 'name' in kwargs.keys():
        nm = kwargs['name']
    else:
        nm = 'box.png'

    if 'scale' in kwargs.keys():
        scl = kwargs['scale']
    else:
        scl = 1e3

    if 'point_size' in kwargs.keys():
        ps = kwargs['point_size']
    else:
        ps = 0.1

    if 'path' in kwargs.keys():
        pth = kwargs['path']
    else:
        pth = '.'

    if 'out_path' in kwargs.keys():
        o_path = kwargs['out_path']
    else:
        o_path = '.'

    fig, ax = plt.subplots(figsize = (20, 20), subplot_kw = {'projection': '3d'}, facecolor = 'black')
    coord = np.array(load_data.load_snap(snap, path = pth, PartType = pt,  param = 'Coordinates')[:])

    ax.scatter(coord[: , 0]/scl, coord[: , 1]/scl, coord[: , 2]/scl, s = ps, alpha = 1,  color = 'white')

    ax.set_facecolor('black')
    ax.set_aspect('equal')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.set_xlabel('x(Mpc)', fontsize = 12)
    ax.set_ylabel('y(Mpc)', fontsize = 12)
    ax.set_zlabel('z(Mpc)', fontsize = 12)

    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    ax.set_zlim(0, 50)

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.zaxis.label.set_color('white')

    ax.tick_params(colors = 'white')

    ax.grid(False)
    plt.savefig(f'{o_path}/{nm}')
    plt.close(fig)

    return None


def __test():
    return None

if __name__ == '__main__':
    __test()