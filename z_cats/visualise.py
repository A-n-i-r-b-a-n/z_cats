import numpy as np
import matplotlib.pyplot as plt
import h5py as h
from PIL import Image
from pathlib import Path
import pyvista as pv
from . import load_data, tools

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
# Plotting 3D interactive box
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
    window_size = (1920, 1080)
    plotter = pv.Plotter(window_size=window_size)
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
        plotter.add_points(cloud, point_size = p, read_points_as_spheres = True)

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
    plotter.add_axes()
    plotter.set_background('black')

    # Keep the physical proportions of the coordinates
    plotter.set_scale(1, 1, 1)

    # Center the camera on the data and fit the entire cloud
    plotter.view_isometric()
    plotter.reset_camera()

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

#################################################################################
# Plotting interactive dm and gas box
#################################################################################
def box_multiparticle(label, dm_data, gas_data, **kwargs):
    """
    The function takes the dark matter coordinates and gas/baryonic matter coordi-
    nates and plots the 3D box with appropriate color code

    label: lsit type, contains the list of labels for x, y and z axes.

    dm_data: numpy ndarray type, refers to the coordinates of the dark matter part-
    icles

    gas_data: numpy ndarray type, refers to the coordinates of the gas/baryonic par-
    ticles 

    sf_data: numpy ndarray type, refers to the coordinates of the star particles.

    dm_color: string/touple/vector type, refers to the color of dm particles.

    gas_color: string/touple/vector type, refers to the color of gas particles.

    sf_color: string/touple/vector type, refers to the color of star particles

    scale: int type, refers to the scale of the box, eg. 1e3 


    """

    if 'dm_color' in kwargs.keys():
        dmc = kwargs['dm_color']
    else:
        dmc = 'red'

    if 'gas_color' in kwargs.keys():
        gc = kwargs['gas_color']
    else:
        gc = 'white'

    if 'bh_color' in kwargs.keys():
        bhc = kwargs['bh_color']
    else:
        bhc = 'blue'
    
    if 'scale' in kwargs.keys():
        scl = kwargs['scale']
    else:
        scl = 1
    
    plotter = pv.Plotter()

    plotter.add_points(
    dm_data/scl, #dm
    color= dmc,
    point_size=1,
    render_points_as_spheres=False,
    opacity=0.35,
    label="High-resolution DM"
)

    plotter.add_points(
    gas_data/scl, #dm
    color= gc,
    point_size=1,
    render_points_as_spheres=False,
    opacity=0.35,
    label="High-resolution gas"
)
    if 'sf_data' in kwargs.keys():

        if 'sf_color' in kwargs.keys():
            sfc = kwargs['sf_color']
        else:
            sfc = 'yellow'
        
        sf_data = kwargs['sf_data']
        plotter.add_points(
        sf_data/scl, #sf
        color= sfc,
        point_size=1,
        render_points_as_spheres=False,
        opacity=0.35,
        label="High-resolution star particles"
        )

    if 'lrdm_data' in kwargs.keys():
        if 'lrdm_color' in kwargs.keys():
            lrdmc = kwargs['lrdm_color']
        else:
            lrdmc = 'gray'
   
        lrdm_data = kwargs['lrdm_data']
        plotter.add_points(
        lrdm_data/scl, #lrdm
        color= lrdmc,
        point_size=1,
        render_points_as_spheres=False,
        opacity=0.35,
        label="Low-resolution dark matter particles"
        )

    if 'bh_data' in kwargs.keys():
            if 'bh_color' in kwargs.keys():
                bhc = kwargs['bh_color']
            else:
                bhc = 'blue'
       
            bh_data = kwargs['lrdm_data']
            plotter.add_points(
            bh_data/scl, #bh
            color= bhc,
            point_size=1,
            render_points_as_spheres=False,
            opacity=0.35,
            label="Black hole particles"
            )

    plotter.set_background('black')

    plotter.show_bounds(
    location='outer',
    xtitle= label[0],
    ytitle= label[1],
    ztitle= label[2],

    color = 'white',
    font_size = 10,
    n_xlabels = 5,
    n_ylabels = 5,
    n_zlabels = 5 )
    plotter.add_axes()
    plotter.show()
    
    return None
#-------------------------------------------------------------------------------#

#################################################################################
# generating png files from a snap
#################################################################################

def create_image(snap, **kwargs):
    """
    Function takes the snapshot number and other parameters and saves the image of
    the point cloud.

    snap: int type; refers to the snapshot number

    PartType: int type; refers to the particle type

    name: string type; refers to the name of the png file saved, default is box.png

    scl: int type; refers to the normalization scales of the displayed axes, defau-
    lt is 1e3

    point_size: float type; refers to the point size to be used in the point cloud d-
    efault is 0.1

    path: string type; refers to the path of the snapshot folder, default is current d-
    irectory

    out_path: string type; refers to the output path of the png file; default is current 
    direcory
    """

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
#------------------------------------------------------------------------------#

################################################################################
# Displaying snapshots pointcloud
################################################################################
def display_image(snap, **kwargs):
    """
    Function takes the snapshot number and other parameters and saves the image of
    the point cloud.

    snap: int type; refers to the snapshot number

    PartType: int type; refers to the particle type

    name: string type; refers to the name of the png file saved, default is box.png

    scl: int type; refers to the normalization scales of the displayed axes, defau-
    lt is 1e3

    point_size: float type; refers to the point size to be used in the point cloud d-
    efault is 0.1

    path: string type; refers to the path of the snapshot folder, default is current d-
    irectory

    """

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
    return None
#-------------------------------------------------------------------------------#

################################################################################
# Group visualisation in a snapshot
################################################################################
def group_vis_marked(gID, snap, **kwargs):
    """
    Function takes group ID and snap number and other parameters to plot a point
    cloud with selected group color coded as red

    gID: int type; refers to the group ID of interest

    snap: int type; refers to the snap number of interest

    path: string type; refers to the path of the snapshot and fof files, default is
    current directory

    scale: float type; refers to the normalization scale of the plot axes

    point_size: float type: refers to the point size of the point cloud

    color: touple/string/hexcode type; refers to the color code of the selected group
    """
    if 'path' in kwargs.keys():
        pth = kwargs['path']
    else:
        pth = '.'

    if 'scale' in kwargs.keys():
        scl = kwargs['scale']
    else:
        scl = 1e3

    if 'point_size' in kwargs.keys():
        ps = kwargs['point_size']
    else:
        ps = 0.1

    if 'color' in kwargs.keys():
        col = kwargs['color']
    else:
        col = 'red'
    
    snap_coords = load_data.load_snap(snap, path = pth, param = 'Coordinates')
    group_coords = tools.ext_group_coord(gID, snap)

    all_partIDs = load_data.load_snap(snap, param = 'ParticleIDs')
    group_partIDs = tools.ext_partID_from_group(snap, gID)

    mask = np.isin(all_partIDs, group_partIDs)
    g_idx = np.where(mask)[0]
    mask2 = ~np.isin(np.arange(len(snap_coords)), g_idx)

    not_group_coords = snap_coords[mask2]

    fig, ax = plt.subplots(figsize = (20, 20), subplot_kw = {'projection': '3d'}, facecolor = 'black')
    
    ax.scatter(not_group_coords[: , 0]/scl, not_group_coords[: , 1]/scl, not_group_coords[: , 2]/scl, 
               s = ps, alpha = 1,  color = 'white')

    ax.scatter(group_coords[: , 0]/scl, group_coords[: , 1]/scl, group_coords[: , 2]/scl, 
               s = ps, alpha = 1,  color = col)

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
    return None
#-------------------------------------------------------------------------------#

def __test():
    print('code ran successfully...')
    return None

if __name__ == '__main__':
    __test()