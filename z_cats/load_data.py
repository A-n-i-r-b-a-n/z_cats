#importing important libraries
import numpy as np
import h5py as h


##########################################################################################
# Loading Snap Files
##########################################################################################

def load_snap(snap, **kwargs):
    """
    Takes in snap number and other arguments to extract the parameters inside an .hdf5 file

    snap: integere type; refers to the snap number

    PartType: integer type; eg. in zoom in gravit only simulations 1 refers to the high res.
    dark matter particles whereas, 2 refers to the low res. dark matter particles

    path: string type; refers to the path where the snap files exist, takes the current dir-
    ectory if no argument is given

    parameter: string type; extracts the particular parameter if mentioned, outputs the enti-
    re dataframe if no argument is given
    """
    if 'path' in kwargs.keys():
        path = kwargs['path']
    else:
        path = '.'

    file = f'{path}/snap_{snap:03d}.hdf5'
    
    if len(kwargs) == 0:
        s = h.File(file, 'r')

    else:

        if 'PartType' in kwargs.keys():
            pt = kwargs['PartType']
        else:
            pt = 1

        if 'param' in kwargs.keys():
            param = kwargs['param']
            s = np.array(h.File(file, 'r')[f'PartType{pt}'][param][:])
        elif 'param' not in kwargs.keys():
            param = kwargs['param']
            print(f"parameter {param} does not exist")
        else: 
            s = h.File(file, 'r')[f'PartType{pt}']

    return s
#--------------------------------------------------------------------------------------------#

##############################################################################################
# Loading FoF files
##############################################################################################
def load_fof(fof_num ):
    fname = f'fof_'
    return None

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





#exectution 

if __name__ == "__main__" :
    print('code ran successfully...')
