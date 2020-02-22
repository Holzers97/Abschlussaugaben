# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:56:27 2020

@author: stefa
"""
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset



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


def months_t(datas):
    """
    Creates a list of monthly temperature

    Parameters
    ----------
    datas : Dataset
        data returned from method read_data(filename).

    Returns
    -------
    Months : list
        list of monthly temperature

    """
    
    temp = datas.variables['air'][372:-1]#starting month is (1979-1948)*12, end is -1 is last, last is not incl.
    temp -= 273
    Months=[]
    for i in range(12):
        Months.append(temp[i::12])
    return Months 


def months_n(datas):
    """
    Creates a list of monthly prate

    Parameters
    ----------
    datas : Dataset
        data returned from method read_data(filename).

    Returns
    -------
    Months : list
        list of monthly prate
    """
    prate = datas.variables['prate'][372:-1]#starting month is (1979-1948)*12, end is -1 is last, last is not incl.
    prate = prate*3600*24
    Months=[]
    for i in range(12):
        Months.append(prate[i::12])
    return Months 


def calc_stats(months):
    """
    

    Parameters
    ----------
    months : list
        list of monthly values.

    Returns
    -------
    avg_months : list
        list of mean value for each month 
    std_months : list
        list of std. derivative for each month

    """
    avg_months=[]
    std_months=[]
    for i in months:
        tmp=np.array(i)
        tmp.flatten()
        avg = np.mean(tmp)
        avg_months.append(avg)
        std = np.std(tmp)
        std_months.append(std)
    return (avg_months , std_months)


def plot_histogramm(temp_mean,temp_std,prate_mean,prate_std):
    '''
    

    Parameters
    ----------
    temp_mean : list
        mean value temp
    temp_std : list
        standart derivative of temp
    prate_mean : list
        mean of percipitation
    prate_std : list
        standart derivative of percipitation

    Returns
    -------
    None.

    '''
    (list_avg,list_std,nied_avg,nied_std)=(temp_mean,temp_std,prate_mean,prate_std)
    
    mon_labels=['Jan','Feb','Mar','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez']
    ax = plt.subplot()
    ax2=plt.twinx()
    ax2.plot(mon_labels,nied_avg,'-b',label='percipitation mean')
    ax2.plot(mon_labels,nied_std,'--b',label='percipitation std')
    ax2.set_ylabel(r'Niederschlag($mm/d$)')    
    ax.plot(mon_labels,list_avg,'-r',label="Temperature mean")
    ax.plot(mon_labels,list_std,"--r",label="Temperature std")
    ax.legend(loc=0)
    ax2.legend(loc=0)
    ax.set_xlabel('Months')
    ax.set_ylabel(r'Tempreture')
    plt.show()


if __name__ == '__main__':
    datas_t= read_data('C:/Users/stefa/Documents/Informathik/air.2m.mon.mean.nc')
    month_t =months_t(datas_t)
    list_avg, list_std = calc_stats(month_t)
    datas_n= read_data('C:/Users/stefa/Documents/Informathik/prate.sfc.mon.mean.nc')
    month_n=months_n(datas_n)
    nied_avg, nied_std = calc_stats(month_n)
    plot_histogramm(list_avg,list_std,nied_avg,nied_std)
