#!/usr/bin/env python3
__all__ = ['read_dms','find_dms_longname']
import numpy as np

def read_dms(dmskey):
    tmp = np.fromfile(dmskey,dtype='<d')
    return tmp

def find_dms_longname(nametag):
    longname_singlelyr_dict = {
            'B0062T':'Total precipitation (mm)',
            'S00030':'Surface albedo (0-1.0) , 12 months ',
            'S00100':'Terrain surface (or ground) temperature (K)',
            'S00300':'Net radiation flux at surface (W/m^2)',
            'S00310':'Net shortwave (solar) flux at the surface (W/m^2)',
            'S00320':'Net longwave (infrared) flux at the surface (W/m^2)',
            'X00740':'Low cloudiness (0.-1.0)',
            'X00770':'Total cloudiness (0.-1.0)',
            }
    longname_vertlyr_dict = {
            '000':'Geopotential height (m)',
            '550':'Cloud liquid water mixing ratio (kg/kg)',
            '551':'Cloud water mixing ratio (kg/kg)',
            '552':'Cloud ice mixing ratio (kg/kg)',
            '553':'Rain mixing ratio (kg/kg)',
            '554':'Snow mixing ratio (kg/kg)',
            '555':'Graupel mixing ratio (kg/kg)',
            '556':'Water vapor mixing ratio (kg/kg)',
            }
    if 'S00' == nametag[:3] or 'X00' == nametag[:3]:
        longname = longname_singlelyr_dict[nametag]
    else:
        vartag = nametag[3:]
        if 'M' == nametag[0]:
            modellv = nametag[1:3] 
            longname = longname_vertlyr_dict[vartag] + ' at level '+modellv
        else:
            plv = nametag[:3]
            if 'H' == plv[0]:
                plv = '1000'
            longname = longname_vertlyr_dict[vartag] + ' at '+ plv + ' hPa'
    
    return longname
