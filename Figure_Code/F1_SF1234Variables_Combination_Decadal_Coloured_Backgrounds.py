#This file will create a stacked line plot of variables for the models in the ensemble

import numpy as np
import xarray as xr
import sys
sys.path.append('/home/jonathan/Documents/Coding/BAS_Coding/Coding/')
from JonTools import data
import cftime
import os
import matplotlib.pyplot as plt
import glob
from matplotlib.offsetbox import AnchoredText



def run_avg(array,period):
    data_run_avg=np.zeros((np.shape(array)[0]-period))
    for j in range(0,np.shape(array)[0]-period):
        data_run_avg[j]=np.mean(array[j:j+period])
    return data_run_avg

InstitutionArray=["BCC","CCCma", "CNRM-CERFACS", "CSIRO", "CSIRO-ARCCSS", "EC-Earth-Consortium", "IPSL", "MIROC", "MIROC", "MPI-M", "MRI", "NASA-GISS", "NCC", "NOAA-GFDL","MOHC","MOHC"]

SourceArray=["BCC-ESM1", "CanESM5", "CNRM-ESM2-1", "ACCESS-ESM1-5", "ACCESS-CM2", "EC-Earth3", "IPSL-CM6A-LR", "MIROC6", "MIROC-ES2L", "MPI-ESM1-2-HR", "MRI-ESM2-0", "GISS-E2-1-G", "NorESM2-MM", "GFDL-CM4","UKESM1-0-LL","HadGEM3-GC31-LL"]

ExptArray=["piControl", "esm-piControl", "esm-piControl", "esm-piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl","piControl", "piControl"]

VariantArray=["r1i1p1f1", "r1i1p1f1", "r1i1p1f2", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f2", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1","r1i1p1f2", "r1i1p1f1"]


VariableArray=["acc","avgmldd0","maxmldd0","lowercircrhon2","siarea"]
VariableNames=["Anatrctic Circumpolar Current Strength/(Sv)","Average Mixed Layer Depth","Maximum Mixed Layer Depth","Lower Circulation Cell Strength","Sea Ice Area"]


panel_labels=["(a)","(b)","(c)","(d)","(e)","(f)","(g)","(h)","(i)","(j)","(k)","(l)","(m)","(n)","(o)","(p)","(q)"]

figsize=(6,6)
small_font=6
reg_font=8
large_font=12


rpa="R"

Data_Path="/home/jonathan/Documents/Data/"
data_path="/home/jonathan/Documents/Data/"
period=10

for j in range(1,len(VariableArray)):
    unit_test=0
    plt.close()
    var_name=VariableArray[j]
    title_name=VariableNames[j]
    print(var_name)
    fig,axs=plt.subplots(nrows=4,ncols=4,sharex=True,sharey=False,figsize=figsize)
    fig.subplots_adjust(hspace=0)
    for i in range(0,len(InstitutionArray)):
        at=AnchoredText(panel_labels[i],prop=dict(size=small_font),frameon=False,loc='upper left')

        values=np.zeros((1))
        row=np.mod(i,4)
        column=np.floor_divide(i,4)
        Institution=InstitutionArray[i]
        source_id=SourceArray[i]
        expt_id=ExptArray[i]
        variant_id=VariantArray[i]
        print(source_id)
        freq="mon"
        spatial="sin"
        source1=source_id
        source2=expt_id
        source3=variant_id
        source_name=source1+"_"+source2+"_"+source3+"_"
        Directory=Data_Path+source_id+"/"+expt_id+"/"+variant_id+"/R/"+var_name
        if len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
            print(Directory,"Contains Files")
            print(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
            Y=xr.open_dataset(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
            X=Y.get(var_name)
            values=X.values
            annual_mean=np.zeros((int(len(values)/12)))
            annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
            running_avg=run_avg(annual_mean,period)
        elif len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
            Y=xr.open_mfdataset("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")
            X=Y.get(var_name)
            values=X.values
            annual_mean=np.zeros((int(len(values)/12)))
            annual_mean=np.mean(np.reshape(values[:(int(len(values)/12))*12],(int(len(values)/12),12)),axis=1)
            running_avg=run_avg(annual_mean,period)
        elif len(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
            print(Directory,"Contains Files")
            print(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
            Y=xr.open_dataset(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
            X=Y.get(var_name)
            values=X.values
            annual_mean=np.zeros((int(len(values)/12)))
            annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
            running_avg=run_avg(annual_mean,period)
        elif len(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
            Y=xr.open_mfdataset("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")
            X=Y.get(var_name)
            values=X.values
            annual_mean=np.zeros((int(len(values)/12)))
            annual_mean=np.mean(np.reshape(values[:(int(len(values)/12))*12],(int(len(values)/12),12)),axis=1)
            running_avg=run_avg(annual_mean,period)

        elif var_name=="acc":
            var_name="accuo"
            Directory=Data_Path+source_id+"/"+expt_id+"/"+variant_id+"/R/"+var_name
            if len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
                print(Directory,"Contains Files")
                print(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
                Y=xr.open_dataset(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
                X=Y.get(var_name)
                values=X.values
                annual_mean=np.zeros((int(len(values)/12)))
                annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
                running_avg=run_avg(annual_mean,period)
            elif len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
                Y=xr.open_mfdataset("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc",combine="by_coords")
                X=Y.get(var_name)
                values=X.values
                annual_mean=np.zeros((int(len(values)/12)))
                annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
                running_avg=run_avg(annual_mean,period)
            elif os.path.exists(Directory)==False:
                print(Directory,"Does Not Exist")
            elif os.listdir(Directory)==[]:
                print(Directory,"Empty")
            var_name="acc"
        if len(values)!=1:
            axs[row,column].plot(np.arange(0,len(running_avg)),running_avg,label=var_name,linewidth=0.2)
        axs[row,column].set_xlim([0,1000])
        axs[row,column].set_ylabel(source_id,fontsize=reg_font,rotation=90,labelpad=0)
        if source_id not in ["MIROC6","MIROC-ES2L","MPI-ESM1-2-HR","MRI-ESM2-0"]:
            axs[row,column].patch.set_facecolor(color="green")
            axs[row,column].patch.set_alpha(0.3)
        axs[column,row].add_artist(at)
        #axs[row,column].tick_params(axis='both',which='both',labelbottom=True)
        if row==3:
            axs[row,column].set_xlabel("time/years",fontsize=reg_font)
            axs[row,column].tick_params(axis='both',which='both',labelbottom=True,labelsize=small_font)
        else:
            axs[row,column].tick_params(axis='both',which='both',labelbottom=False,labelsize=small_font)

        if i==unit_test and len(values)!=1:
            units=X.units
        else:
            unit_test=unit_test+1

    fig.suptitle("Decadal plots of "+title_name+"/("+units+")",fontsize=large_font)
    #plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=True)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.subplots_adjust(hspace=0,wspace=0.50)

    plt.savefig("/home/jonathan/Documents/Figures/Thesis_Specific_Figures/CanESM5/"+var_name+"_Combo_Figure_decadal_coloured_plots.eps",format="eps")
    plt.savefig("/home/jonathan/Documents/Figures/Thesis_Specific_Figures/CanESM5/"+var_name+"_Combo_Figure_decadal_coloured_plots.pdf",dpi=300)
