#!/usr/bin/env python3
__all__ = ['read_dms','find_dms_longname']
import numpy as np

def read_dms(dmskey):
    tmp = np.fromfile(dmskey,dtype='<d')
    return tmp

def find_dms_longname(nametag):
    longname_dict = {
            'S00300':'Net radiation flux at surface (W/m^2)',
            'S00310':'Net shortwave (solar) flux at the surface (W/m^2)',
            'S00320':'Net longwave (infrared) flux at the surface (W/m^2)',
            }
    longname = longname_dict[nametag]
    return longname
