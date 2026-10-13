import numpy as np
import h5py as h


####################################################
# Extracyion of particle Ids from a giben group ID #
####################################################

def ext_partID_from_group(snap, group_id, **kwargs):

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



#########################################################
# Performing Unwrapping Operation                       #
#########################################################

def unwarp(axis, l_box):
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


############################################################
#  Computing r_offset r_extent and r_center                #
############################################################

def ref_params(x, y, z, l_box):

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

    ref_extent = ref_max - ref_min
    ref_center = (ref_min + ref_max) / 2

    # Normalize for MUSIC
    ref_offset_norm = ref_min / l_box
    ref_extent_norm = ref_extent / l_box
    ref_center_norm = ref_center/l_box
    
    print("ref_center =", ref_center_norm)
    print("ref_offset =", ref_offset_norm)
    print("ref_extent =", ref_extent_norm)

    return ref_center_norm, ref_extent_norm, ref_offset_norm


