__all__ = [
    'ndate','setup_cmap','cnbestF','latlon_news','lat_ns','lon_we','gen_eqs_by_stats',
    'find_cnlvs','get_dates', 'cubicSplineInterpolate', 'haversineDistance',
]
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

earthR = 6371.  # km

def get_dates(sdate, edate, hint):
    from datetime import datetime, timedelta
    date1 = pd.to_datetime(sdate,format='%Y%m%d%H')
    date2 = pd.to_datetime(edate,format='%Y%m%d%H')
    delta = timedelta(hours=hint)
    dates = pd.date_range(start=date1, end=date2, freq=delta)
    return dates


def ndate(hinc, cdate):
    from datetime import datetime
    from datetime import timedelta
    yy=int(str(cdate)[:4])
    mm=int(str(cdate)[4:6])
    dd=int(str(cdate)[6:8])
    hh=int(str(cdate)[8:10])
    dstart=datetime(yy,mm,dd,hh)
    dnew=dstart+timedelta(hours=hinc)
    dnewint=int(str('%4.4d' % dnew.year)+str('%2.2d' % dnew.month)+
                str('%2.2d' %dnew.day)+str('%2.2d' % dnew.hour))
    return dnewint


def setup_cmap(name, valuelst, idxlst):
    #
    # Set colormap through NCL colormap and index
    #
    import os, platform
    from pathlib import Path
    import matplotlib.colors as mpcrs
    import numpy as np
    rootpath=Path(__file__).parent
    nclcmap=str(rootpath.resolve())+'/colormaps'
    
    cmapname=name
    f=open(nclcmap+'/'+cmapname+'.rgb','r')
    a=[]
    for line in f.readlines():
        if ('ncolors' in line):
            clnum=int(line.split('=')[1])
        a.append(line)
    f.close()
    values = [x/(valuelst[-1]-valuelst[0]) for x in valuelst]
    b = a[-clnum:]
    c = []
    if ('MPL' in name or 'GMT' in name):
        for idx in idxlst:
            if (i == 0):
                c.append(tuple(float(y) for y in [1,1,1]))
            elif (i == 1):
                c.append(tuple(float(y) for y in [0,0,0]))
            elif (i == -1):
                c.append(tuple(float(y) for y in [0.5,0.5,0.5]))
            else:
                c.append(tuple(float(y) for y in b[idx-2].split('#', 1)[0].split()))
    else:
        for idx in idxlst:
            if (idx == 0):
                c.append(tuple(float(y)/255. for y in [255, 255, 255]))
            elif (idx == 1):
                c.append(tuple(float(y)/255. for y in [0, 0, 0]))
            elif (idx == -1):
                c.append(tuple(round(float(y)/255., 4) for y in [128, 128, 128]))
            else:
                c.append(tuple(round(float(y)/255., 4) 
                                     for y in b[idx-2].split('#', 1)[0].split()))

    d = mpcrs.LinearSegmentedColormap.from_list(name, c, len(idxlst))
    return c, d

def cnbestF(data):
    import numpy as np
    std=np.nanstd(data)
    mean=np.nanmean(data)
    vmax=np.nanmax(abs(data))
    if (vmax>5*(mean+std*3)):
        cnvmax=mean+std*4
    else:
        cnvmax=vmax
    ccnvmax='%e'%(cnvmax)
    tmp1=ccnvmax.find('-')
    tmp2=ccnvmax.find('+')
    if (tmp1<0):
        tmp=tmp2
    if (tmp2<0):
        tmp=tmp1
    d=int(ccnvmax[tmp:])
    cnmaxF=np.ceil(float(ccnvmax[:tmp-1]))*10**d
    return cnmaxF

def latlon_news(plat,plon):
    deg_sym=u'\u00B0'
    if (plat > 0.):
        ns='N'
    elif (plat < 0.):
        ns='S'
    else:
        ns=''
    if (plon > 0.):
        we='E'
    elif (plon < 0.):
        we='W'
    else:
        we=''
    txlat='%.2f%s %s'%(abs(plat),deg_sym,ns)
    txlon='%.2f%s %s'%(abs(plon),deg_sym,we)
    return txlat,txlon

def lat_ns(plat):
    deg_sym=u'\u00B0'
    if (plat > 0.):
        ns='N'
    elif (plat < 0.):
        ns='S'
    else:
        ns=''
    txlat='%.f%s %s'%(abs(plat),deg_sym,ns)
    return txlat

def lon_we(plon):
    deg_sym=u'\u00B0'
    if (plon > 0.):
       we='E'
    elif (plon < 0.):
       we='W'
    else:
       we=''
    txlon='%.f%s %s'%(abs(plon),deg_sym,we)
    return txlon

def gen_eqs_by_stats(stats_in):
    if (stats_in.intercept<0):
       fiteqs='$y=%.2fx–%.2f$' %(stats_in.slope,abs(stats_in.intercept))
    elif (stats_in.intercept>0):
       fiteqs='$y=%.2fx+%.2f$' %(stats_in.slope,abs(stats_in.intercept))
    else:
       fiteqs='y=%.2f*x' %(stats_in.slope)
    return fiteqs

def find_cnlvs(indata,topq=None,ntcks=None,eqside=None):
    if not topq: topq=0.997
    if not ntcks: ntcks=21
    if not eqside: eqside=0
    tmpmax=np.nanquantile(indata,topq)
    tmpmin=np.nanquantile(indata,1-topq)
    print(tmpmin,tmpmax)
    if ( abs(tmpmax)<1. and tmpmax!=0. ):
       ndecimals=int(abs(np.floor(np.log10(abs(tmpmax)))))
       cnlvmax=round(tmpmax,ndecimals)
    else:
       cnlvmax=np.sign(tmpmax)*(np.ceil(abs(tmpmax)))
    if ( abs(tmpmin)<1. and tmpmin!=0. ):
       ndecimals=int(abs(np.floor(np.log10(abs(tmpmin)))))
       cnlvmin=round(tmpmin,ndecimals)
    else:
       cnlvmin=np.sign(tmpmin)*(np.ceil(abs(tmpmin)))
    print(cnlvmin,cnlvmax)
    if (eqside):
        cnlvmax=np.max((abs(cnlvmin),abs(cnlvmax)))
        cnlvs=np.linspace(-cnlvmax,cnlvmax,ntcks)
    else:
        if (cnlvmax*cnlvmin<0):
            h_ntcks=int(ntcks*0.5)
            if ( np.mod(ntcks,2)==0 ):
               neg_lvs=np.linspace(cnlvmin,0,h_ntcks,endpoint=False)
               pos_int=(abs(cnlvmax)/int(ntcks*0.5))
               pos_lvs=np.arange(0+pos_int,cnlvmax+pos_int,pos_int)
            else:
               neg_lvs=np.linspace(cnlvmin,0,h_ntcks,endpoint=False)
               pos_lvs=np.linspace(0,cnlvmax,h_ntcks+1)
            cnlvs=np.append(neg_lvs,pos_lvs)
        else:
            print('Warning max=%.f, min=%.f' %(cnlvmax,cnlvmin))
            cnlvs=np.linspace(cnlvmin,cnlvmax,ntcks)
    print(cnlvs)
    return cnlvs

def oprval_parse(indata=None, oprval_str=None):
    import operator
    import re

    ops = {
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
    }

    pattern = r'(>=|<=|!=|==|>|<)(\d+(\.\d+)?)'
    match = re.match(pattern, oprval_str)

    opr = match.group(1)
    val = match.group(2)

    boolarr = ops[opr](indata, val)
    return boolarr

# Functions setup
def cubicSplineInterpolate(row):
    x = select_aeronet_wvl
    y = row[['440nm', '500nm', '675nm']].values
    spline = CubicSpline(x, y)
    return float(spline(target_wvl))
    
def haversineDistance(row):
    lat1 = np.radians(row['latitude'])
    lon1 = np.radians(row['longitude'])
    lat2 = np.radians(ref_lat)
    lon2 = np.radians(ref_lon)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return earthR * c
