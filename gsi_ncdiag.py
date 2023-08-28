__all__ = ['read_rad_ncdiag','read_cnv_ncdiag','read_rad_ncdiag0']

import numpy as np
import xarray as xa

def read_rad_ncdiag0(infile,**kwargs):
    # Read in the old converted NetCDF diagnostic files
    select_wavenumber = kwargs.get('chkwvn',None)
    cal_ae = kwargs.get('cal_ae',False)
    get_water_frac = kwargs.get('get_water_frac',False) 

    ds=xa.open_dataset(infile)
    npts=ds.obsloc.size
    nchs=ds.channel.size
    rlat=ds.locinfo[0,:].values
    rlon=ds.locinfo[1,:].values
    rlon=(rlon+180)%360-180
    qcflags=ds.qcflag.values.T
    obs=ds.tb_obs.values.T
    varinv=ds.errinv.values.T
    omb_bc=ds.tbc.values.T
    omb_nbc=ds.tbcnob.values.T
    sim=obs-omb_nbc
    clr=sim
    if cal_ae:
       aereff_fg=sim-clr
       aereff_obs=obs-clr
       aereff=0.5*abs(aereff_fg)+0.5*abs(aereff_obs)
    if get_water_frac: water_frac=ds.locinfo[10,:].values

    data_dict={'rlon':(['obsloc'],rlon),
               'rlat':(['obsloc'],rlat),
               'qcflag':(['obsloc','wavenumber'],qcflags),
               'tb_obs':(['obsloc','wavenumber'],obs),
               'tb_sim':(['obsloc','wavenumber'],sim),
               'tb_clr':(['obsloc','wavenumber'],clr),
               'varinv':(['obsloc','wavenumber'],varinv),
               'omb_bc':(['obsloc','wavenumber'],omb_bc),
               'omb_nbc':(['obsloc','wavenumber'],omb_nbc),
               }
    if cal_ae: data_dict['Ae']=(['obsloc','wavenumber'],aereff)
    if get_water_frac: data_dict['water_frac']=(['obsloc'],water_frac)

    coords_dict={'obsloc':np.arange(npts),'wavenumber':ds.wavenumber.values}

    tmpds=xa.Dataset(data_dict,coords=coords_dict)
    
    if type(select_wavenumber)==list or type(select_wavenumber)==float:
       tmpds=tmpds.sel(wavenumber=select_wavenumber)

    return tmpds

def read_rad_ncdiag(infile,**kwargs):
    # Read in the new NetCDF diagnostic files
    area = kwargs.get('area',None)
    cornerll = kwargs.get('cornerll',None)
    select_wavenumber = kwargs.get('chkwvn',None)
    select_qcflag = kwargs.get('sel_qc',-1)
    cal_ae = kwargs.get('cal_ae',False)
    get_water_frac = kwargs.get('get_water_frac',False) 
    if area != 'Glb':
        minlat, maxlat, minlon, maxlon = cornerll

    ds=xa.open_dataset(infile)
    npts=int(ds.nobs.size/ds.nchans.size)
    nchs=ds.nchans.size
    rlat=np.reshape(ds.Latitude.values,(npts,nchs))
    rlon=np.reshape(ds.Longitude.values,(npts,nchs))
    rlon=(rlon+180)%360-180
    qcflags=np.reshape(ds.QC_Flag.values,(npts,nchs))
    obs=np.reshape(ds.Observation.values,(npts,nchs))
    sim=np.reshape(ds.Simulated_Tb.values,(npts,nchs))
    clr=np.reshape(ds.Clearsky_Tb.values,(npts,nchs))
    varinv=np.reshape(ds.Inverse_Observation_Error.values,(npts,nchs))
    omb_bc=np.reshape(ds.Obs_Minus_Forecast_adjusted.values,(npts,nchs))
    omb_nbc=np.reshape(ds.Obs_Minus_Forecast_unadjusted.values,(npts,nchs))

    mask = (~np.isnan(rlat))
    if area != 'Glb':
        mask = mask&((rlon<maxlon)&(rlon>minlon)&(rlat>minlat)&(rlat<maxlat))
    if select_qcflag != -1:
        mask = mask&(qcflag==select_qcflag)
    if sel_bufr != 'all'
        mask = mask&(obstype==int(bufrtype))
    npts = rlat[mask].size

    if cal_ae:
       aereff_fg=sim-clr
       aereff_obs=obs-clr
       aereff=0.5*abs(aereff_fg)+0.5*abs(aereff_obs)
    if get_water_frac: water_frac=np.reshape(ds.Water_Fraction.values,(npts,nchs))

    data_dict={'rlon':(['obsloc'],rlon[mask,0]),
               'rlat':(['obsloc'],rlat[mask,0]),
               'qcflag':(['obsloc','wavenumber'],qcflags[mask]),
               'tb_obs':(['obsloc','wavenumber'],obs[mask]),
               'tb_sim':(['obsloc','wavenumber'],sim[mask]),
               'tb_clr':(['obsloc','wavenumber'],clr[mask]),
               'varinv':(['obsloc','wavenumber'],varinv[mask]),
               'omb_bc':(['obsloc','wavenumber'],omb_bc[mask]),
               'omb_nbc':(['obsloc','wavenumber'],omb_nbc[mask]),
               }

    if cal_ae: data_dict['Ae']=(['obsloc','wavenumber'],aereff)
    if get_water_frac: data_dict['water_frac']=(['obsloc','wavenumber'],water_frac)

    coords_dict={'obsloc':np.arange(npts),'wavenumber':ds.wavenumber.values}

    tmpds=xa.Dataset(data_dict,coords=coords_dict)
    
    if select_wavenumber is not None: 
       if (type(select_wavenumber)==list or
           type(select_wavenumber)==float or 
           select_wavenumber.size>0):
          tmpds=tmpds.sel(wavenumber=select_wavenumber)

    return tmpds

def read_cnv_ncdiag(infile,**kwargs):
    useqc = kwargs.get('useqc',None)
    sel_bufr = kwargs.get('sel_bufr',None)
    is_sfc = kwargs.get('is_sfc',None)
    is_uv = kwargs.get('is_uv',None)
    area = kwargs.get('area',None)
    cornerll = kwargs.get('cornerll',None)
    if area != 'Glb':
        minlat, maxlat, minlon, maxlon = cornerll

    ds = xa.open_dataset(infile)
    rlat = ds.Latitude.data
    rlon = ds.Longitude.data
    rlon = (rlon+180)%360-180
    sta_id = ds.Station_ID.data
    obstype = ds.Observation_Type.data
    sta_elev = ds.Station_Elevation.data
    qcflag = ds.Analysis_Use_Flag.data
    errinv = ds.Errinv_Final.data
    obs = ds.Observation.data
    omb_bc = ds.Obs_Minus_Forecast_adjusted.data
    omb_nbc = ds.Obs_Minus_Forecast_unadjusted.data

    mask = (~np.isnan(rlat))
    if area != 'Glb':
        mask = mask&((rlon<maxlon)&(rlon>minlon)&(rlat>minlat)&(rlat<maxlat))
    if useqc:
        mask = mask&(qcflag==1)
    if sel_bufr != 'all'
        mask = mask&(obstype==int(bufrtype))
    npts = rlat[mask].size

    data_dict = {'rlon':(['obsloc'],rlon[mask]),
                 'rlat':(['obsloc'],rlat[mask]),
                 'qcflag':(['obsloc'],qcflag[mask]),
                 'obs':(['obsloc'],obs[mask]),
                 'omb_bc':(['obsloc'],omb_bc[mask]),
                 'omb_nbc':(['obsloc'],omb_nbc[mask]),
                 'sta_id':(['obsloc'],sta_id[mask]),
                 'obstype':(['obsloc'],obstype[mask]),
                 }
    if not is_sfc: 
       pres = ds.Pressure.data
       data_dict['pres'] = (['obsloc'],pres[mask])

    coords_dict = {'obsloc':np.arange(npts)}

    tmpds = xa.Dataset(data_dict,coords=coords_dict)

    return tmpds

