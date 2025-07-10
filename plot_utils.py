import matplotlib.pyplot as plt
import numpy as np

__all__ = ['set_size', 'pltprof', 'plthist', 'plt_x2y', 'setupax_2dmap', 'plt_x2cf', 'plt_scatter', 'plt_hist2d']

minussign=u'\u2212'


def set_size(w,h, ax=None, l=None, r=None, t=None, b=None):
    """ w, h: width, height in inches """
    if not ax: ax=plt.gca()
    if not l:
       l = ax.figure.subplotpars.left
    else:
       ax.figure.subplots_adjust(left=l)
    if not r:
       r = ax.figure.subplotpars.right
    else:
       ax.figure.subplots_adjust(right=r)
    if not t:
       t = ax.figure.subplotpars.top
    else:
       ax.figure.subplots_adjust(top=t)
    if not b:
       b = ax.figure.subplotpars.bottom
    else:
       ax.figure.subplots_adjust(bottom=b)
       
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)


def pltprof(yval,y_name,y_unit,xval,x_name,x_unit,clrlst,lglbs,title,y_invert,ax=None,fig=None):
    if not fig: fig=plt.gcf()
    if not ax: ax=plt.gca()
    if (y_invert):
       ax.invert_yaxis()
    ax.set_prop_cycle(color=clrlst)
    ax.plot(xval,yval,'o-')
    ax.ticklabel_format(axis="x", style="sci", scilimits=(0,0), useMathText=True)
    ax.tick_params(axis='both')
    ax.xaxis.get_offset_text().set_visible(False)
    fig.canvas.draw()
    x_offtx=ax.xaxis.get_offset_text().get_text()
    y_offtx=ax.yaxis.get_offset_text().get_text()
    xlb=''; xlb=xlb.join([x_name,' [',x_offtx,x_unit,']'])
    ylb=''; ylb=ylb.join([y_name,' [',y_offtx,y_unit,']'])
    ax.set_xlabel(xlb)
    ax.set_ylabel(ylb)
    if (lglbs != ''):
       ax.legend(lglbs)
    ax.grid()
    ax.set_title(title,loc='left')
    return fig,ax


def plthist(data,binlvs,title,outname):
    fig=plt.figure()
    plt.hist(data,binlvs)
    plt.title(title,loc='left')
    fig.savefig(outname,dpi=300)
    plt.close()


def setupax_2dmap(cornerlatlon,area,proj,lbsize=None):
    import cartopy.crs as ccrs
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    if not lbsize: lbsize=20

    minlat=cornerlatlon[0]; maxlat=cornerlatlon[1]
    minlon=cornerlatlon[2]; maxlon=cornerlatlon[3]
    fig=plt.figure()
    ax=plt.subplot(projection=proj)
    ax.coastlines(resolution='110m')
    if ( area == 'Glb' ):
        ax.set_global()
    else:
        ax.set_extent((minlon,maxlon,minlat,maxlat),crs=proj)
    gl=ax.gridlines(draw_labels=True,dms=True,x_inline=False, y_inline=False)
    gl.right_labels=False
    gl.top_labels=False
    # gl.xformatter=LongitudeFormatter(degree_symbol=u'\u00B0 ')
    # gl.yformatter=LatitudeFormatter(degree_symbol=u'\u00B0 ')
    gl.xlabel_style={'size':lbsize}
    gl.ylabel_style={'size':lbsize}

    return fig,ax,gl


def plt_x2y(yval,ylb,x1val,x1lb,x2val,x2lb,prop_dict,title,yinvert,xrefs,**kwargs):
    fig=kwargs.get('fig',None)
    ax=kwargs.get('ax',None)
    if not fig: fig=plt.gcf()
    if not ax: ax=plt.gca()

    lgloc=kwargs.get('lgloc',0)
    fill_std=kwargs.get('fill_std',False)
    if 'pltstdv' not in yval.keys() and fill_std:
       print('stdv is not available',flush=1)
       fill_std=False
    plot_diff=kwargs.get('plot_diff',False)

    pltdata=yval.pltdata.data.swapaxes(0,1)
    if plot_diff:
       datadiff=pltdata[:,1]-pltdata[:,0]
    if fill_std:
       pltstdv=yval.pltstdv.data.swapaxes(0,1)

    xaxis=np.arange(x1val.size)
    if (yinvert):
       ax.invert_yaxis()
    color_list=prop_dict['color']
    lnsty_list=prop_dict['line_style']
    lnwid_list=prop_dict['line_width']
    mrker_list=prop_dict['marker']
    mksiz_list=prop_dict['mark_size']
    lgend_list=prop_dict['legend']
    flsty_list=prop_dict['fillstyle']
    ax.set_prop_cycle(color=color_list,linestyle=lnsty_list,linewidth=lnwid_list,
                      marker=mrker_list,markersize=mksiz_list,fillstyle=flsty_list)

    ax.set_xlabel(x1lb)
    ax.set_ylabel(ylb)
    ax.set_title(title,loc='left')
    ax.set_xlim(xaxis[0],xaxis[-1])
    ax.grid(axis='x')
    ax.plot(xaxis,pltdata)
    if fill_std:
       for i in np.arange(pltdata.shape[1]):
           tmpdata=pltdata[:,i]; tmpstdv=pltstdv[:,i]
           ax.fill_between(xaxis,tmpdata-1*tmpstdv,tmpdata+1*tmpstdv,color=color_list[i],alpha=0.2)

    if (len(xrefs)!=0):
       ax.vlines(xrefs,0,1,transform=ax.get_xaxis_transform(),linestyle='dashed',linewidth=1.)

    xtickspos=ax.get_xticks()
    x1labels=[]
    for n in xtickspos:
        if (n>x1val.size):
           n=x1val.size-n
        x1labels.append('%.2f'%(x1val[int(n)]))   
    ax.legend(lgend_list,loc=lgloc)
    ax.set_xticklabels(x1labels)
    x2labels=[]
    for n in xtickspos:
        if (n>x1val.size):
           n=x1val.size-n
        x2labels.append('%.2f'%(x2val[int(n)]))
    ax2=ax.twiny()
    ax2.set_xticks(xtickspos)
    ax2.set_xticklabels(x2labels)
    ax2.set_xlim(xaxis[0],xaxis[-1])
    ax2.xaxis.set_ticks_position('bottom')
    ax2.xaxis.set_label_position('bottom')
    ax2.spines['bottom'].set_position(('outward', 48))
    ax2.set_xlabel(x2lb)

    if plot_diff:
       ax3=ax.twinx()
       ax3.plot(xaxis,datadiff,'--k')
       ax3.set_xlabel('%s%s%s' %(lgend_list[1],minussign,lgend_list[0]))
       ax3.hlines(0.,0,1,transform=ax3.get_yaxis_transform(),colors='grey',linewidth=0.4,linestyle='dashed')

    return fig,ax,ax2


def plt_x2cf(zval,yval,ylb,x1val,x1lb,x2val,x2lb,cnlvs,clrmap,cnnorm,cbasp,cblb,title,outname,yinvert,fig=None,ax=None):
    if not fig: fig=plt.gcf()
    if not ax: ax=plt.gca()
    xaxis=np.arange(x1val.size)
    if (yinvert):
       ax.invert_yaxis()
    ax.set_xlabel(x1lb)
    ax.set_ylabel(ylb)
    ax.set_title(title,loc='left')
    ax.set_xlim(xaxis[0],xaxis[-1])
    cn=ax.contourf(xaxis,yval,zval,'-',levels=cnlvs,cmap=clrmap,norm=cnnorm,extend='both')
    fig.colorbar(cn,ax=ax,orientation='vertical',aspect=cbasp,ticks=cnlvs,label=cblb,format='%.1e',pad=0.02)
    xtickspos=ax.get_xticks()
    x1labels=[]
    for n in xtickspos:
        if (n>x1val.size):
           n=x1val.size-n
        x1labels.append('%.2f'%(x1val[int(n)]))
    ax.set_xticklabels(x1labels)

    x2labels=[]
    for n in xtickspos:
        if (n>x1val.size):
           n=x1val.size-n
        x2labels.append('%.2f'%(x2val[int(n)]))
    ax2=ax.twiny()
    ax2.set_xticks(xtickspos)
    ax2.set_xticklabels(x2labels)
    ax2.set_xlim(xaxis[0],xaxis[-1])
    ax2.xaxis.set_ticks_position('bottom')
    ax2.xaxis.set_label_position('bottom')
    ax2.spines['bottom'].set_position(('outward', 48))
    ax2.set_xlabel(x2lb)
    fig.savefig(outname,dpi=300)
    plt.close()


def plt_scatter(xval,yval,pltdata,clrmap,title,fname,fsize):
    fig=plt.figure(figsize=fsize,constrained_layout=1)
    ax=plt.subplot()
    sc=ax.scatter(xval,yval,c=pltdata,s=25,cmap=clrmap,norm=cnnorm)
    plt.colorbar(sc,orientation='vertical',fraction=0.025)
    #plt.colorbar(sc,orientation=cbori,fraction=0.06)
    ax.set_title(title,loc='left')
    fig.savefig(fname,dpi=200)


def plt_hist2d(dataframe, x, y, axis, save, savename, **kwargs):
    x_data = dataframe[x]
    y_data = dataframe[y]
    xlbstr = kwargs.get('xlb', x)
    ylbstr = kwargs.get('ylb', y)
    hist2d, x_edge, y_edge = np.histogram2d(x_data,
                                            y_data,
                                            bins=axis)

    cnlvs = np.linspace(0, hist2d.max(), 256)
    clrnorm = mpcrs.BoundaryNorm(cnlvs, len(cnlvs), extend='max')

    fig, ax = plt.subplots()
    set_size(5, 5, b=0.1, l=0.1, r=0.95, t=0.95)
    cn = ax.contourf(axis[:-1], axis[:-1], hist2d.swapaxes(0,1),
                     levels=cnlvs, norm=clrnorm, cmap=white_gist_earth,
                     extend='max')
    plt.plot(
        [0.0, hist2d_xmax],
        [0.0, hist2d_xmax],
        color='gray',
        linewidth=2,
        linestyle='--'
    )
    plt.xlim(0.01, hist2d_xmax)
    plt.ylim(0.01, hist2d_xmax)

    if hist2d_in_log:
        ax.set_xscale('log')
        ax.set_yscale('log')
    ax.set_aspect('equal')

    plt.grid(alpha=0.5)
    plt.xlabel(xlbstr, fontsize=11)
    plt.ylabel(ylbstr, fontsize=11)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    correlation_matrix = np.corrcoef(x_data, y_data)
    correlation_xy = correlation_matrix[0, 1]
    r_squared = correlation_xy ** 2
    bias = np.mean(y_data) - np.mean(x_data)
    rbias = bias/np.mean(x_data)
    ssize = len(x_data)

    stats_dict = {
        'Counts': str("%.0f" % ssize),
        'Absolute Bias': str("%.3f" % bias),
        'Relative Bias': str("%.3f" % rbias),
        'R': str("%.3f" % correlation_xy),
        'R\u00b2': str("%.3f" % r_squared),
    }
    x_pos = 0.012
    y_pos = 1.02
    for key in stats_dict.keys():
        stat_str = '%s= %s' %(key, stats_dict[key])
        y_pos = y_pos - 0.05
        ax.annotate(stat_str, (x_pos, y_pos), ha='left', va='center', 
                    fontsize=12, xycoords='axes fraction')

    cb = plt.colorbar(cn, orientation='horizontal', fraction=0.03, aspect=30, 
                      pad=0.12, extend='max', ticks=cnlvs[::50])
    cb.ax.minorticks_off()
    cb.ax.ticklabel_format(axis='x', style='sci', scilimits=(0, 0),
                           useMathText=True)

    if save:
        plt.savefig(savename, dpi=quality)
    plt.close(fig)
    return
