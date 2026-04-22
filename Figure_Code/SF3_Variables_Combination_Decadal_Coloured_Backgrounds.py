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
from scipy.stats import pearsonr


def lag_corr(X,Y,lag):
    if lag>0:
        result=pearsonr(X[:-lag],Y[lag:])
    elif lag<0:
        result=pearsonr(X[abs(lag):],Y[:-abs(lag)])
    elif lag==0:
        result=pearsonr(X,Y)
    return result



def run_avg(array,period):
    data_run_avg=np.zeros((np.shape(array)[0]-period))
    for j in range(0,np.shape(array)[0]-period):
        data_run_avg[j]=np.mean(array[j:j+period])
    return data_run_avg

InstitutionArray=["BCC","CCCma", "CNRM-CERFACS", "CSIRO", "CSIRO-ARCCSS", "EC-Earth-Consortium", "IPSL", "MIROC", "MIROC", "MPI-M", "MRI", "NASA-GISS", "NCC", "NOAA-GFDL","MOHC","MOHC"]

SourceArray=["BCC-ESM1", "CanESM5", "CNRM-ESM2-1", "ACCESS-ESM1-5", "ACCESS-CM2", "EC-Earth3", "IPSL-CM6A-LR", "MIROC6", "MIROC-ES2L", "MPI-ESM1-2-HR", "MRI-ESM2-0", "GISS-E2-1-G", "NorESM2-MM", "GFDL-CM4","UKESM1-0-LL","HadGEM3-GC31-LL"]

ExptArray=["piControl", "esm-piControl", "esm-piControl", "esm-piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl","piControl", "piControl"]

VariantArray=["r1i1p1f1", "r1i1p1f1", "r1i1p1f2", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f2", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1","r1i1p1f2", "r1i1p1f1"]


VariableArray=["acc","avgmldd0","maxmldd0","lowercircrhon2","siarea","uppercircrhon2","wwmax","namoc","namoc26n"]
VariableNames=["Antarctic Circumpolar Current Strength","Average Mixed Layer Depth","Maximum Mixed Layer Depth","Lower Circulation Cell Strength","Sea Ice Area","Lower Circulation Cell Strength","Westerly Wind Max","Atlantic Meridional Overturning Circulation","Atlantic Meridional Overturning Circulation"]


#panel_labels=["(a)","(b)","(c)","(d)","(e)","(f)","(g)","(h)","(i)","(j)","(k)","(l)","(m)","(n)","(o)","(p)","(q)"]

panel_labels=["(a)","(e)","(i)","(m)","(b)","(f)","(j)","(n)","(c)","(g)","(k)","(o)","(d)","(h)","(l)","(p)"]


figsize=(6,6)
small_font=6.5
reg_font=6.5
large_font=12
max_lag=60
lags=np.arange(-int(max_lag),int(max_lag+1))


rpa="R"

Data_Path="/home/jonathan/Documents/Data/"
data_path="/home/jonathan/Documents/Data/"
period=10

for j in range(7,8):
    unit_test=0
    plt.close()
    var_name=VariableArray[j]
    title_name=VariableNames[j]
    print(var_name)
    fig,axs=plt.subplots(nrows=4,ncols=4,sharex=True,sharey=False,figsize=figsize)
    fig.subplots_adjust(hspace=0)
    for i in range(0,len(InstitutionArray)):
        try:
            var_name=VariableArray[j]
            #at=AnchoredText(panel_labels[i],prop=dict(size=small_font),frameon=False,loc='upper left')

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
                if var_name=="namoc":
                    annual_mean=annual_mean/10**9
                running_avg=run_avg(annual_mean,period)
            elif len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
                Y=xr.open_mfdataset("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")
                X=Y.get(var_name)
                values=X.values
                annual_mean=np.zeros((int(len(values)/12)))
                annual_mean=np.mean(np.reshape(values[:(int(len(values)/12))*12],(int(len(values)/12),12)),axis=1)
                if var_name=="namoc":
                    annual_mean=annual_mean/10**9
                
                running_avg=run_avg(annual_mean,period)
            elif len(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
                print(Directory,"Contains Files")
                print(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
                Y=xr.open_dataset(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
                X=Y.get(var_name)
                values=X.values
                annual_mean=np.zeros((int(len(values)/12)))
                annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
                if var_name=="namoc":
                    annual_mean=annual_mean/10**9                
                running_avg=run_avg(annual_mean,period)
            elif len(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
                Y=xr.open_mfdataset("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")
                X=Y.get(var_name)
                values=X.values
                annual_mean=np.zeros((int(len(values)/12)))
                annual_mean=np.mean(np.reshape(values[:(int(len(values)/12))*12],(int(len(values)/12),12)),axis=1)
                if var_name=="namoc":
                    annual_mean=annual_mean/10**9
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
            #axs[row,column].set_ylabel(source_id,fontsize=reg_font,rotation=90,labelpad=0)
            if source_id not in ["MIROC6","MIROC-ES2L","MPI-ESM1-2-HR","MRI-ESM2-0"]:
                axs[row,column].patch.set_facecolor(color="green")
                axs[row,column].patch.set_alpha(0.3)
            #axs[column,row].add_artist(at)
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
            var_name="acc"
            Directory=Data_Path+source_id+"/"+expt_id+"/"+variant_id+"/R/"+var_name
            if len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
                print(Directory,"Contains Files")
                print(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
                Y=xr.open_dataset(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
                X=Y.get(var_name)
                values=X.values
                acc_annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
            elif len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
                Y=xr.open_mfdataset("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")
                X=Y.get(var_name)
                values=X.values
                acc_annual_mean=np.mean(np.reshape(values[:(int(len(values)/12))*12],(int(len(values)/12),12)),axis=1)
            elif len(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
                print(Directory,"Contains Files")
                print(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
                Y=xr.open_dataset(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
                X=Y.get(var_name)
                values=X.values
                acc_annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)

            elif len(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
                Y=xr.open_mfdataset("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")
                X=Y.get(var_name)
                values=X.values
                acc_annual_mean=np.mean(np.reshape(values[:(int(len(values)/12))*12],(int(len(values)/12),12)),axis=1)

            elif var_name=="acc":
                var_name="accuo"
                Directory=Data_Path+source_id+"/"+expt_id+"/"+variant_id+"/R/"+var_name
                if len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
                    print(Directory,"Contains Files")
                    print(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
                    Y=xr.open_dataset(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
                    X=Y.get(var_name)
                    values=X.values
                    acc_annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
                elif len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
                    Y=xr.open_mfdataset("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc",combine="by_coords")
                    X=Y.get(var_name)
                    values=X.values
                    acc_annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
                elif os.path.exists(Directory)==False:
                    print(Directory,"Does Not Exist")
                elif os.listdir(Directory)==[]:
                    print(Directory,"Empty")
                var_name="acc"
            lag_corr_values=np.zeros((2*max_lag+1))
            lag_corr_p_values=np.zeros((2*max_lag+1))
            min_len=np.nanmin((len(acc_annual_mean),len(annual_mean)))
            for l in range(0,2*max_lag+1):
                lag_corr_values[l],lag_corr_p_values[l]=lag_corr(run_avg(acc_annual_mean[:min_len],period),run_avg(annual_mean[:min_len],period),l-max_lag)
            max_val=np.nanmax(lag_corr_values)
            min_val=np.nanmin(lag_corr_values)
            if max_val > -min_val:
                lag_corr_mag=max_val
                lag_position=np.where(lag_corr_values==lag_corr_mag)[0]-max_lag
            elif max_val < -min_val:
                lag_corr_mag=min_val
                lag_position=np.where(lag_corr_values==lag_corr_mag)[0]-max_lag
            ymin, ymax = axs[row,column].get_ylim()
            del acc_annual_mean, annual_mean
            print(source_id,ymin,ymax)
            axs[row,column].set_ylim(ymin, ymax+((ymax-ymin)*0.2))
            at2=AnchoredText(panel_labels[i]+" "+source_id+f"\n lag: {lag_position[0]} corr: {lag_corr_mag:.2f}",prop=dict(size=small_font),frameon=False,loc='upper left',bbox_to_anchor=(0.005,0.995),bbox_transform=axs[row,column].transAxes,borderpad=0)
            axs[row,column].add_artist(at2)
            var_name=VariableArray[j]
            if row != 3:
                axs[row,column].tick_params(axis="x",which="both",bottom=False, top=False,labelbottom=False)

        except Exception as e:
            print(f"{source_id} {VariableArray[j]} An error occurred: {e}")
            print(source_id+"_"+VariableArray[j])

    if var_name=="namoc":
        units="Sv"
    fig.suptitle("Decadal plots of "+title_name+"/("+units+")",fontsize=large_font)
    #plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=True)
    #plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.subplots_adjust(hspace=0.02,wspace=0.35,top=0.95,right=0.975,left=0.08)

    plt.savefig("/home/jonathan/Documents/Figures/Forced_Paper/"+VariableArray[j]+"_Combo_Figure_decadal_coloured_plots.eps",format="eps")
    plt.savefig("/home/jonathan/Documents/Figures/Forced_Paper/"+VariableArray[j]+"_Combo_Figure_decadal_coloured_plots.pdf",dpi=300)
