#!/usr/bin/env python3
__all__ = ['opendap_m2_aod']
import xarray as xa
import pandas as pd
from datetime import datetime, timedelta


def opendap_m2_aod(sdate,edate,hint,area,varname,**kwargs):
    outfmt = kwargs.get('outfmt','2d')
    cornerll = kwargs.get('cornerll','None')
    if area != 'Glb' and cornerll is None:
        raise Exception('Any subregion other than global (Glb) need to specify corner lat/lon')
    else:
        minlat, maxlat, minlon, maxlon = cornerll

    m2_url = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXAER.5.12.4'
    m2tag = 'tavg1_2d_aer_Nx'
    
    offset = timedelta(minutes=30)
    date1 = pd.to_datetime(sdate,format='%Y%m%d%H')+offset
    date2 = pd.to_datetime(edate,format='%Y%m%d%H')+offset
    delta = timedelta(hours=hint)
    dates = pd.date_range(start=date1, end=date2, freq=delta)

    p_pdy='00000000'
    fileslist=[]
    for date in dates:
        yy=date.strftime('%Y') ; mm=date.strftime('%m') ; dd=date.strftime('%d') ; hh=date.strftime('%H')
        pdy=date.strftime('%Y%m%d')
        if (yy=='2020' and mm=='09'):
           m2ind='401'
        else:
           m2ind='400'
    
    #/2020/09/MERRA2_401.tavg1_2d_aer_Nx.20200901.nc4'
        if (pdy!=p_pdy):
           p_pdy=pdy
           fileslist.append('{}/{}/{}/MERRA2_{}.{}.{}{}{}.nc4'.format(m2_url,yy,mm,m2ind,m2tag, yy, mm, dd))

    ds = xa.open_mfdataset(fileslist)
    print('Succeed accessing MERRA2 OPeNDAP dataset',flush=1)
    ds = ds.sel(time=dates)
    if (area!='Glb'):
        ds = ds.sel(lat=slice(minlat,maxlat),lon=slice(minlon,maxlon))

    if (outfmt == 'ts'):
        data = ds[varname].mean(dim=['lat','lon'])
    elif (outfmt == 'zonal'):
        data = ds[varname].mean(dim=['time','lon'])
    elif (outfmt == 'meri'):
        data = ds[varname].mean(dim=['time','lat'])
    elif (outfmt == '2d'):
        data = ds[varname].mean(dim=['time'])
    else:
        raise Exception('Not available output type')
 
    return data
