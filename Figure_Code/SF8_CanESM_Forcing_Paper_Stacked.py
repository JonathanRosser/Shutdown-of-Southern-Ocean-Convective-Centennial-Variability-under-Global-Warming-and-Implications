#This file creates annual mean plots comparing deep convection calculations to mixed layer depth calculations

import numpy as np
import xarray as xr
import sys
sys.path.append('/home/jonathan/Documents/Coding/BAS_Coding/Coding/')
from JonTools import data
import cftime
import os
import matplotlib.pyplot as plt
import glob
from scipy.stats import pearsonr


def run_avg(array,period):
    data_run_avg=np.zeros((np.shape(array)[0]-period))
    for j in range(0,np.shape(array)[0]-period):
        data_run_avg[j]=np.mean(array[j:j+period])
    return data_run_avg

def lag_corr(X,Y,lag):
    if lag>0:
        result=pearsonr(X[:-lag],Y[lag:])
    elif lag<0:
        result=pearsonr(X[abs(lag):],Y[:-abs(lag)])
    elif lag==0:
        result=pearsonr(X,Y)
    return result



InstitutionArray=["BCC","CCCma", "CNRM-CERFACS", "CSIRO", "CSIRO-ARCCSS", "EC-Earth-Consortium", "IPSL", "MIROC", "MIROC", "MPI-M", "MRI", "NASA-GISS", "NCC", "NOAA-GFDL","MOHC","MOHC"]

SourceArray=["BCC-ESM1", "CanESM5", "CNRM-ESM2-1", "ACCESS-ESM1-5", "ACCESS-CM2", "EC-Earth3", "IPSL-CM6A-LR", "MIROC6", "MIROC-ES2L", "MPI-ESM1-2-HR", "MRI-ESM2-0", "GISS-E2-1-G", "NorESM2-MM", "GFDL-CM4","UKESM1-0-LL","HadGEM3-GC31-LL"]

ExptArray=["piControl", "esm-piControl", "esm-piControl", "esm-piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl","piControl", "piControl"]

VariantArray=["r1i1p1f1", "r1i1p1f1", "r1i1p1f2", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f2", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1","r1i1p1f2", "r1i1p1f1"]

VariableArray=['acc','avgdensity40s50s','avgdensity65','wwmax','maxmld','lowercircrhon','h65s']


TitleArray=['ACC/Sv',"Average Density \n40$^{\circ}$S-50$^{\circ}$S/kgm$^{-3}$","Average Density \n south of 65$^{\circ}$S/kgm$^{-3}$",'Max Westerly Wind Stress/(Nm$^{-2}$)','Maximum Southern Ocean \n Mixed Layer Depth/m','Lower Circulation/(kg/s)','Ocean Heat South of 65$^{\circ}$S/J']

min_line_values=(54, 148, 235, 337, 429, 546, 637, 740, 832, 932)
max_line_values=(4, 101, 194, 290, 387, 502, 597,694, 780,881, 983)


rpa="R"
period=10
Data_Path="/home/jonathan/Documents/Data/"
data_path="/home/jonathan/Documents/Data/"
for i in range(1,2):
    Institution=InstitutionArray[i]
    source_id=SourceArray[i]
    expt_id=ExptArray[i]
    variant_id=VariantArray[i]
    freq="mon"
    spatial="sin"
    source1=source_id
    source2=expt_id
    source3=variant_id
    source_name=source1+"_"+source2+"_"+source3+"_"
    data=[]
    names=[]
    for j in range(0,len(VariableArray)):
        var_name =VariableArray[j]
        title_name=TitleArray[j]
        Directory=Data_Path+source_id+"/"+expt_id+"/"+variant_id+"/R/"+var_name
        if os.path.exists(Directory)==False:
            print(Directory,"Does Not Exist")
        elif os.listdir(Directory)==[]:
            print(Directory,"Empty")
        elif len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
            print(Directory,"Contains Files")
            print(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
            Y=xr.open_dataset(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
            X=Y.get(var_name)
            values=X.values
            annual_mean=np.zeros((int(len(values)/120)))
            annual_mean=np.mean(np.reshape(values[:(int(len(values)/12))*12],(int(len(values)/12),12)),axis=1)
            decadal_mean=run_avg(annual_mean,period)
            data.append(decadal_mean)
            names.append(title_name)
        elif len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
            Y=xr.open_mfdataset("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")

            X=Y.get(var_name)
            values=X.values
            annual_mean=np.zeros((int(len(values)/12)))
            annual_mean=np.mean(np.reshape(values[:(int(len(values)/12))*12],(int(len(values)/12),12)),axis=1)
            decadal_mean=run_avg(annual_mean,period)
            data.append(decadal_mean)
            names.append(title_name)

        else:
            print(Directory,"None of the Above")


    max_lag=25
    NumVar=len(data)
    plt.close()
    fig,axs=plt.subplots(NumVar,sharex=True,gridspec_kw={'hspace': 0},figsize=(16,16))
    fig.suptitle("Decadal Averages for Weddell Sea Related Variables in CanESM5",fontsize=24)
    for k in range(0,NumVar):
        plot_data=data[k]
        lag_corr_values=np.zeros((2*max_lag+1))
        sig_values=np.zeros((2*max_lag+1))
        for l in range(0,2*max_lag+1):
            lag_corr_values[l],sig_values[l]=lag_corr(data[0],data[k],l-max_lag)
        max_val=np.nanmax(lag_corr_values)
        min_val=np.nanmin(lag_corr_values)
        if max_val > -min_val:
            lag_corr_mag=max_val
            lag_position=np.where(lag_corr_values==lag_corr_mag)[0]-max_lag
            sig=sig_values[np.where(lag_corr_values==lag_corr_mag)[0]]
        elif max_val < -min_val:
            lag_corr_mag=min_val
            lag_position=np.where(lag_corr_values==lag_corr_mag)[0]-max_lag
            sig=sig_values[np.where(lag_corr_values==lag_corr_mag)[0]]
        print(lag_corr_mag,lag_position,sig)
        axs[k].plot(np.arange(0,500),plot_data[:500],label=names[k],color='k')
        axs[k].label_outer()
        axs[k].set_ylabel(names[k],fontsize=18,rotation=60,labelpad=80,wrap=True)
        axs[k].tick_params(axis='both',which='major',labelsize=14)
        for l in range(0,len(min_line_values)):
            axs[k].axvline(x=min_line_values[l],color='b',alpha=0.4)
        for l in range(0,len(max_line_values)):
            axs[k].axvline(x=max_line_values[l],color='r',alpha=0.4)
        axs[k].set_xlim([0,500])
        axs[k].set_ylim([axs[k].get_ylim()[0],axs[k].get_ylim()[1]+(axs[k].get_ylim()[1]-axs[k].get_ylim()[0])*0.08])
        if k !=0:
            x_text_position = axs[k].get_xlim()[0] + 0.05 * (axs[k].get_xlim()[1] - axs[k].get_xlim()[0])
            y_text_position = axs[k].get_ylim()[0] + 0.90 * (axs[k].get_ylim()[1] - axs[k].get_ylim()[0])
            axs[k].text(x_text_position,y_text_position,"corr: "+str(lag_corr_mag)[:5]+" lag: "+str(lag_position[0]),fontsize=14)
    axs[NumVar-1].set_xlabel("Time/years",fontsize=18)
    plt.tight_layout(rect=[0.01, 0.01, 1, 0.95])
    #plt.show()
    plt.savefig("/home/jonathan/Documents/Figures/Combo/CanESM_Figs/CanESM_Forcings_Paper_Fig.pdf")






