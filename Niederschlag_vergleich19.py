# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 14:38:04 2020

@author: stefa
"""
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from  mpl_toolkits.basemap import Basemap


def read_data(filename):
    '''
    reads the data from website

Parameters
    ----------
    filename : strg
        path and filename

Returns
    -------
    data : Dataset netCDF4._netCDF4.Dataset
            

'''
    data=Dataset(filename, mode= 'r')
    return data
    
def mean_per(datas):
    """
    returns mean temperature of the data from 1979 - 2019


Parameters
    ----------
    datas : Dataset netCDF4._netCDF4.Dataset
        raw data from read_data(filename) method

Returns
    -------
    temp_av_1979_2019 : MaskedArray
        mean value for given data

"""
    perc = datas.variables['prate'][372:-1]#starting month is (1979-1948)*12, end is -1 is last, last is not incl.
    perc = perc*3600*24#umrechnung mm/tag
    #takes mean for each time with fix lat and lon.
    perc_1979_2019 = np.mean(perc[:,:,:],axis = 0)
    
    perc_19 = datas.variables['prate'][841:-1]#takes all months from 2019
    perc_19 = perc_19*3600*24
    perc_19_m = np.mean(perc_19[:,:,:],axis = 0)
    
    perc_com = perc_19_m - perc_1979_2019
    return perc_com
    
def plot_stuff(datas, mean_perc):
    """
        

Parameters
    ----------
    datas : netCDF4._netCDF4.Dataset
        raw data from input file returned by read_data(filename)
    mean_temp : MaskedArray
    DESCRIPTION.

Returns
    -------
    None.

"""
    plt.figure(figsize=(20,10))
    map = Basemap(projection="cyl", resolution='l', llcrnrlat=-90, urcrnrlat=90,llcrnrlon=0, urcrnrlon=361, ) 
    #map = Basemap(projection="cyl", resolution='c', llcrnrlon=-180, urcrnrlon=180) 
    map.drawcoastlines(color="white") 
    lons,lats = np.meshgrid(datas.variables['lon'][:], datas.variables['lat'][:]) 
    x,y = map(lons, lats)
    map.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=12)
    map.drawmeridians(np.arange(0, 360, 360/6.), labels=[0,0,0,1], fontsize=12)
    
    temp_plot = map.contourf(x, y, mean_perc, cmap=plt.cm.viridis) 
    cb = map.colorbar(temp_plot, "right", size="5%", pad="2%", extend = 'both')
    cb.set_label(u"$mm/d$",fontsize=24)
    plt.title("Mean Percipitation rate(1979-2019) compared with 2019´s mean Percipitations rate",fontsize=20)
    #plt.annotate('Data - CRU TS v4.02',(-178,-88), fontsize=6)
    plt.show() 
    #plt.savefig("cruts_global.png")
    
if __name__=="__main__":
    daten = read_data('C:/Users/stefa/Documents/Informathik/prate.sfc.mon.mean.nc')
    avg_temp = mean_per(daten)
    plot_stuff(daten,avg_temp)


