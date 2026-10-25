import numpy as np
import h5py as h
from . import load_data

####################################################
# Extracyion of particle Ids from a given group ID #
####################################################

def ext_partID_from_group(snap, group_id, **kwargs):
    """
    snap: int type, refers to the snap number

    group_id: int type, refers to the group ID
    
    path: str type, takes the path where the snaps exist
    """ 

    if 'path' in kwargs.keys():
        pth = kwargs['path']
    else:
        pth = '.'

    f = f'{pth}/fof_subhalo_tab_{snap:03d}.hdf5'
    fof_dat = h.File(f, 'r')
    membership = fof_dat['Group']['GroupLen'][group_id]

    lst = np.arange(0, group_id)
    start_indx = 0
    for i in lst:
        start_indx += fof_dat['Group']['GroupLen'][i]

    stop_indx = start_indx + membership

    ids = fof_dat['IDs']['ID'][start_indx: stop_indx]
    fof_dat.close()
    
    return ids
#-------------------------------------------------------#

#########################################################
# Performing Unwrapping Operation                       #
#########################################################

def unwarp(axis, l_box):
    """

    Unwraps lagrangian region if it crosses the periodic boundaries
    axis = numpy ndarrat type, refers to the axis to unwrap

    l_box: int type, refers to the size of the simulation volume in kpc
    """
    a = axis

    #finding the largest gap
    a_sorted = np.sort(a)
    gaps = np.diff(a_sorted)

    #processing
    i = np.argmax(gaps)
    a_max_left = a_sorted[i]
    mask_a_lg = (a <= a_max_left)

    a_new = a.copy()

    # Shift the low-a part across the periodic boundary
    a_new[mask_a_lg] += l_box
    return a_new 
#----------------------------------------------------------#

############################################################
#  Computing r_offset r_extent and r_center                #
############################################################

def ref_params(x, y, z, l_box, **kwargs):
    """
    Takes x, y and z axis, and box length as input to com-
    pute the ref parameters to be given in the MUSIC param 
    file

    x: numpy ndarray type, refers to the unwrapped x axis

    y: numpy ndarray type, refers to the unwrapped y axis

    z: numpy ndarray type, refers to the unwrapped z axis

    l_box: int type, refers to the size of the simulation 
    box in kpc

    buffer: float type, range (0 - 1), adds a buffer aro- 
    und the extent ofthe lagrangian region
    """

    if 'buffer' in kwargs.keys():
        buff = kwargs['buffer']
    else:
        buff = 1

    ref_min = np.array([
        x.min(),
        y.min(),
        z.min()
    ])

    ref_max = np.array([
        x.max(),
        y.max(),
        z.max()
    ])

    extent = ref_max - ref_min
    buffer = buff*extent

    l_min = ref_min - buffer
    l_max = ref_max + buffer

    ref_center = (l_min + l_max) / 2
    ref_extent = l_max - l_min

    # Normalize for MUSIC
    ref_center_norm = ref_center/l_box
    ref_extent_norm = ref_extent / l_box
    ref_offset_norm = l_min / l_box
    
    
    print("ref_center =", ref_center_norm)
    print("ref_extent =", ref_extent_norm)
    print("ref_offset =", ref_offset_norm)

    return ref_center_norm, ref_extent_norm, ref_offset_norm
#---------------------------------------------------------------#

#################################################################
# Extract particle coordinates from a group
#################################################################
def ext_group_coord(gID, snap):
    """
    The function takes group ID and snapshot number to extract 
    the coordinates of the particles in a particle snapshot

    gID: int type; refers to the group ID of interest
    snap: int type; refers to the snapshot number 
    """

    #extract the the coordinates of all particles in the snapshot
    snap_coord  = load_data.load_snap(snap, param = 'Coordinates')
    #extract the snap particle ID data
    snap_part_IDs = load_data.load_snap(snap, param = 'ParticleIDs')
    #extracting the particle IDs of a given group
    g_part_IDs = ext_partID_from_group(snap, gID)
    #creating a particle mask to filter out the coordinates 
    #associated with particle IDs of a given group
    part_mask = np.isin(snap_part_IDs, g_part_IDs)

    #filtering out the coordinates of the particles associated
    #with a given group
    g_coords = snap_coord[part_mask]
    return g_coords
#-------------------------------------------------------------------#

def __test():
    print('code ran successfully...')
    return None

if __name__ == '__main__':
    __test()