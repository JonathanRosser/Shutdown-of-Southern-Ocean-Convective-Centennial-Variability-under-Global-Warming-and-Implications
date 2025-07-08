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
import math


def run_avg(array,period):
    data_run_avg=np.zeros((np.shape(array)[0]-period))
    for j in range(0,np.shape(array)[0]-period):
        data_run_avg[j]=np.mean(array[j:j+period])
    return data_run_avg

def var_load(source_id,expt_id,variant_id,var_name):
    rpa="R"
    freq="mon"
    spatial="sin"
    source1=source_id
    source2=expt_id
    source3=variant_id
    source_name=source1+"_"+source2+"_"+source3+"_"
    Data_Path="/home/jonathan/Documents/Data_Improved/"
    Directory=Data_Path+source_id+"/"+expt_id+"/"+variant_id+"/R/"+var_name
    if source_id=="MIROC6" and var_name=="lowercircrhon2":
        var_name="lowercircrhon2uo"
    #elif source_id=="CanESM5" and var_name=="lowercircrhon2":
    #    var_name="lowercircrhon2uo"

    if len(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
        print(Directory,"Contains Files")
        print(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
        Y=xr.open_dataset(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
        X=Y.get(var_name)
        #if var_name != "wfo_vol_change_div_binned" and var_name !="hflux_walin_volchange_sigma2binned":
        values=X.values
        annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
        return annual_mean
    elif len(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
        Y=xr.open_mfdataset("/home/jonathan/Documents/Data_Improved/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")

        X=Y.get(var_name)

        values=X.values
        annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
        return annual_mean
    elif len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
        print(Directory,"Contains Files")
        print(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
        Y=xr.open_dataset(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
        X=Y.get(var_name)
        values=X.values
        annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
        return annual_mean
    elif len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
        Y=xr.open_mfdataset("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")
        X=Y.get(var_name)
        values=X.values
        annual_mean=np.mean(np.reshape(values,(int(len(values)/12),12)),axis=1)
        return annual_mean


def source_plot(institution_id,source_id,control_expt_id,control_variant_id,variant_list,ssp119_variant_list,ssp126_variant_list,ssp245_variant_list,ssp585_variant_list,var_name,loc_index,institution_number):

    try:
        if var_name=="acc":
            try:
                control_values=run_avg(var_load(source_id,control_expt_id,control_variant_id,var_name),10)
            except:
                control_values=run_avg(var_load(source_id,control_expt_id,control_variant_id,"accuo"),10)
        elif var_name[-5:]=="mldd0":
            load_values=var_load(source_id,control_expt_id,control_variant_id,var_name)
            for j in range(0,len(load_values)):
                if load_values[j]<0:
                    load_values[j]=load_values[j]*-1
            control_values=run_avg(load_values,10)
        else:
            control_values=run_avg(var_load(source_id,control_expt_id,control_variant_id,var_name),10)
        #if np.nanmean(control_values)<0:
        #    control_values=-control_values
        #plt.boxplot(control_values,positions=[-5],widths=5,whis=(0,100))
        plt.plot(np.nanstd(control_values))
    except:
        print(institution_id,source_id,control_expt_id,control_variant_id,var_name,"failed")
    
    plt.ylabel(source_id)
    plt.xlim(1850,2100)
    expt_id="historical"
    data=[]
    max_len=0
    for j in range(0,len(variant_list)):
        variant_id=variant_list[j]
        try:
            if var_name=="acc" and source_id=="CanESM5" and variant_id!="r1i1p1f1":
                init_data=var_load(source_id,expt_id,variant_id,var_name)
                for k in range(0,len(init_data)):
                    if init_data[k]<0:
                        init_data[k]=init_data[k]*-1000
                var_data=run_avg(init_data,10)
            elif var_name=="acc":
                try:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                except:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,"accuo"),10)
            else:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
            #if np.nanmean(var_data)<0:
            #    var_data=-var_data
            if var_name=="acc" and np.nanmean(var_data)<0.5:
                var_data=var_data*1000
            if var_name=="acc" and source_id=="HadGEM3-GC31-LL" and np.nanmean(var_data)<0:
                var_data=var_data*-1
            if np.nanmean(var_data)!=0:
                data.append(var_data)
                max_len=np.nanmax((len(var_data),max_len))
                #plt.plot(var_data,color="grey",alpha=0.4)
        except:
            print(institution_id,source_id,expt_id,variant_id,var_name,"failed")
    data_array=np.zeros((len(data),max_len))
    data_array.fill(np.nan)
    for j in range(0,len(data)):
        length=len(data[j])
        data_array[j,:length]=data[j]
    indices=np.arange(1850,1850+max_len,1)
    plt.plot(indices,np.nanstd(data_array,axis=0),color="k")
    expt_id="ssp119"
    data=[]
    min_len=300
    for j in range(0,len(ssp119_variant_list)):
        variant_id=ssp119_variant_list[j]
        try:
            if var_name=="acc" and source_id=="CanESM5" and variant_id!="r1i1p1f1":
                init_data=var_load(source_id,expt_id,variant_id,var_name)
                for k in range(0,len(init_data)):
                    if init_data[k]<0:
                        init_data[k]=init_data[k]*-1000
                var_data=run_avg(init_data,10)
            elif var_name=="acc":
                try:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                except:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,"accuo"),10)
            else:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
            #if np.nanmean(var_data)<0:
            #    var_data=-var_data
            if var_name=="acc" and np.nanmean(var_data)<0.5:
                var_data=var_data*1000
            if np.nanmean(var_data)!=0:
                data.append(var_data)
                min_len=np.nanmin((len(var_data),min_len))
                indices=np.arange(2015,2015+len(var_data),1)
                #plt.plot(indices,var_data,color="c",alpha=0.2)
        except:
            print(institution_id,source_id,expt_id,variant_id,var_name,"failed")

    data_array=np.zeros((len(data),min_len))
    for j in range(0,len(data)):
        data_array[j,:]=data[j][:min_len]
    indices=np.arange(2015,2015+min_len,1)
    ssp119_indices=indices
    ssp119_values=np.nanstd(data_array,axis=0)
    expt_id="ssp126"
    data=[]
    min_len=300
    for j in range(0,len(ssp126_variant_list)):
        variant_id=ssp126_variant_list[j]
        try:
            if var_name=="acc" and source_id=="CanESM5" and variant_id!="r1i1p1f1":
                init_data=var_load(source_id,expt_id,variant_id,var_name)
                for k in range(0,len(init_data)):
                    if init_data[k]<0:
                        init_data[k]=init_data[k]*-1000
                var_data=run_avg(init_data,10)
            elif var_name=="acc":
                try:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                except:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,"accuo"),10)
            else:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
            #if np.nanmean(var_data)<0:
            #    var_data=-var_data
            if var_name=="acc" and np.nanmean(var_data)<0.5:
                var_data=var_data*1000
            if np.nanmean(var_data)!=0:
                data.append(var_data)
                min_len=np.nanmin((len(var_data),min_len))
                indices=np.arange(2015,2015+len(var_data),1)
                #plt.plot(indices,var_data,color="b",alpha=0.2)
        except:
            print(institution_id,source_id,expt_id,variant_id,var_name,"failed")

    data_array=np.zeros((len(data),min_len))
    for j in range(0,len(data)):
        data_array[j,:]=data[j][:min_len]
    indices=np.arange(2015,2015+min_len,1)
    ssp126_indices=indices
    ssp126_values=np.nanstd(data_array,axis=0)

    expt_id="ssp245"
    data=[]
    min_len=300
    for j in range(0,len(ssp245_variant_list)):
        variant_id=ssp245_variant_list[j]
        try:
            if var_name=="acc" and source_id=="CanESM5" and variant_id!="r1i1p1f1":
                init_data=var_load(source_id,expt_id,variant_id,var_name)
                for k in range(0,len(init_data)):
                    if init_data[k]<0:
                        init_data[k]=init_data[k]*-1000
                var_data=run_avg(init_data,10)
            elif var_name=="acc":
                try:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                except:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,"accuo"),10)
            else:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
            #if np.nanmean(var_data)<0:
            #    var_data=-var_data
            if var_name=="acc" and np.nanmean(var_data)<0.5:
                var_data=var_data*1000
            if np.nanmean(var_data)!=0:
                data.append(var_data)
                min_len=np.nanmin((len(var_data),min_len))
                indices=np.arange(2015,2015+len(var_data),1)
                #plt.plot(indices,var_data,color="sandybrown",alpha=0.2)
        except:
            print(institution_id,source_id,expt_id,variant_id,var_name,"failed")

    data_array=np.zeros((len(data),min_len))
    for j in range(0,len(data)):
        data_array[j,:]=data[j][:min_len]
    indices=np.arange(2015,2015+min_len,1)
    ssp245_indices=indices
    ssp245_values=np.nanstd(data_array,axis=0)

    expt_id="ssp585"
    data=[]
    min_len=300
    for j in range(0,len(ssp585_variant_list)):
        variant_id=ssp585_variant_list[j]
        try:
            if var_name=="acc" and source_id=="CanESM5" and variant_id!="r1i1p1f1":
                init_data=var_load(source_id,expt_id,variant_id,var_name)
                for k in range(0,len(init_data)):
                    if init_data[k]<0:
                        init_data[k]=init_data[k]*-1000
                var_data=run_avg(init_data,10)
            elif var_name=="acc":
                try:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                except:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,"accuo"),10)
            else:
                    var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
            #if np.nanmean(var_data)<0:
            #    var_data=-var_data
            if var_name=="acc" and np.nanmean(var_data)<0.5:
                var_data=var_data*1000
            if var_name=="acc" and source_id=="HadGEM3-GC3.1-LL" and np.nanmean(var_data)<0:
                var_data=var_data*-1
            if np.nanmean(var_data)!=0:
                data.append(var_data)
                min_len=np.nanmin((len(var_data),min_len))
                indices=np.arange(2015,2015+len(var_data),1)
                #plt.plot(indices,var_data,color="red",alpha=0.2)
        except:
            print(institution_id,source_id,expt_id,variant_id,var_name,"failed")

    data_array=np.zeros((len(data),min_len))
    for j in range(0,len(data)):
        data_array[j,:]=data[j][:min_len]
    indices=np.arange(2015,2015+min_len,1)
    ssp585_indices=indices
    ssp585_values=np.nanstd(data_array,axis=0)

    plt.plot(ssp119_indices,ssp119_values,color="blue")
    plt.plot(ssp126_indices,ssp126_values,color="midnightblue")
    plt.plot(ssp245_indices,ssp245_values,color="darkorange")
    plt.plot(ssp585_indices,ssp585_values,color="darkred")
    plt.title(source_id)
    plt.xticks(())
    #plt.xticks(np.array((0,30,60,90,150,180,210,240)),("0","30","60","90","150","180","210","240"))
    #plt.xlim(-15,240)
    plt.grid()
    if source_id=="MRI-ESM2-0" and var_name=="acc":
        plt.ylim(130,160)
    elif source_id=="MRI-ESM2-0" and var_name=="weddellgyreuo":
        plt.ylim(1.8*10**11,2.2*10**11)





#VariableArray=["acc", "rsiarea", "sst_thetao", "weddellgyre", "rossgyre", "siarea", "wsiarea", "ewmax", "ewpos", "maccpos", "naccpos", "saccpos", "wwmax", "wwpos","avgmld","w_avgmld","w_maxmld","maxmld","r_maxmld","a_maxmld"]

#TitleArray=["acc", "rsiarea", "sst_thetao", "weddellgyre", "rossgyre", "siarea", "wsiarea", "ewmax", "ewpos", "maccpos", "naccpos", "saccpos", "wwmax", "wwpos","avgmld","w_avgmld","w_maxmld","maxmld","r_maxmld","a_maxmld"]


#VariableArray=["lowercircrhon2","uppercircrhon2"]

#TitleArray=["lowercircrhon2","uppercircrhon"]


VariableArray=["whflux","rhflux","hflux"]
TitleArray=["Weddell Heat Flux", "Ross Heat Flux", "Heat Flux south of 50$^{\circ}$S"]

VariableArray=["r_avgmldd0", "avgmldd0", "w_maxmldd0", "w_avgmldd0", "r_maxmldd0", "maxmldd0", "l_maxmldd0", "a_maxmldd0", "siarea"]
TitleArray=["Ross mean mld", "Mean mld south of 50S/m", "Weddell max mld", "Weddel mean mld", "Ross max mld", "Max MLD south of 50$^{\circ}$S", "Labrador max mld", "Arctic max mld", "Sea Ice Area"]


#VariableArray=["acc","siarea","avgmldd0","maxmldd0","w_avgmldd0","r_avgmldd0","lowercircrhon2","uppercircrhon2","weddellgyre","weddellgyreuo","rossgyre","rossgyreuo"]
#TitleArray=["acc","siarea","avgmldd0","maxmldd0","w_avgmldd0","r_avgmldd0","lowercircrhon2","uppercircrhon2","weddellgyre","weddellgyreuo","rossgyre","rossgyreuo"]

VariableArray=["acc","maxmldd0","lowercircrhon2","lowercircrhon2uo"]
TitleArray=["ACC/ Sv","maxmldd0","lowercircrhon2","lowercircrhon2uo"]

#VariableArray=["weddellgyre","weddellgyreuo"]
#TitleArray=["Weddell Gyre/(kg/s)","Weddell Gyre/(kg/s)"]

#VariableArray=["lowercircrhon2"]
#TitleArray=["Lower Circulation Cell/(kg/s)"]


rpa="R"
institution_id_list=[
    "CCCma",
    "CSIRO-ARCCSS",
    "CSIRO",
    "EC-Earth-Consortium",
    "NOAA-GFDL",
    "MOHC",
    "IPSL",
    "MIROC",
    "MRI",
    "MOHC"
    ]
source_id_list=[
    "CanESM5",
    "ACCESS-CM2",
    "ACCESS-ESM1-5",
    "EC-Earth3",
    "GFDL-CM4",
    "HadGEM3-GC31-LL",
    "IPSL-CM6A-LR",
    "MIROC6",
    "MRI-ESM2-0",
    "UKESM1-0-LL"
    ]
control_expt_list=[
    "piControl",
    "piControl",
    "esm-piControl",
    "piControl",
    "piControl",
    "piControl",
    "piControl",
    "piControl",
    "piControl",
    "piControl"
    ]
control_variant_list=[
        "r1i1p1f1",
        "r1i1p1f1",
        "r1i1p1f1",
        "r1i1p1f1",
        "r1i1p1f1",
        "r1i1p1f1",
        "r1i1p1f1",
        "r1i1p1f1",
        "r1i1p1f1",
        "r1i1p1f2"
        ]
hist_variant_id_list_of_lists=[
        ["r1i1p1f1", "r1i1p2f1", "r2i1p1f1", "r2i1p2f1", "r3i1p1f1", "r3i1p2f1", "r4i1p1f1", "r4i1p2f1",  "r5i1p1f1", "r5i1p2f1", "r6i1p1f1", "r6i1p2f1", "r7i1p1f1", "r7i1p2f1", "r8i1p1f1", "r8i1p2f1", "r9i1p1f1", "r9i1p2f1", "r10i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f3","r5i1p1f3","r11i1p1f3","r25i1p1f3"],
        ["r1i1p1f1", "r2i1p1f1", "r3i1p1f1", "r4i1p1f1", "r5i1p1f1", "r6i1p1f1", "r7i1p1f1", "r8i1p1f1", "r9i1p1f1"],
        ["r1i1p1f1", "r2i1p1f1", "r3i1p1f1", "r4i1p1f1", "r5i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f2","r2i1p1f2","r3i1p1f2","r4i1p1f2","r5i1p1f3","r6i1p1f3","r7i1p1f3","r8i1p1f2","r9i1p1f2","r10i1p1f2","r11i1p1f2","r12i1p1f2","r16i1p1f2","r17i1p1f2","r18i1p1f2","r19i1p1f2"]
        ]

ssp119_variant_id_list_of_lists=[
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1", "r4i1p1f1", "r5i1p1f1"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ]

ssp126_variant_id_list_of_lists=[
        ["r1i1p1f1", "r1i1p2f1", "r2i1p1f1", "r2i1p2f1", "r3i1p1f1", "r3i1p2f1", "r4i1p1f1", "r4i1p2f1",  "r5i1p1f1", "r5i1p2f1", "r6i1p1f1", "r6i1p2f1", "r7i1p1f1", "r7i1p2f1", "r8i1p1f1", "r8i1p2f1", "r9i1p1f1", "r9i1p2f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f1"],
        [],
        ["r1i1p1f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        [],
        ["r1i1p1f1"],
        ["r1i1p1f2","r2i1p1f2", "r3i1p1f2", "r4i1p1f2", "r5i1p1f2"],
        ]

ssp245_variant_id_list_of_lists=[
        ["r1i1p1f1","r3i1p1f1","r3i1p2f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f1","r2i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f3","r2i1p1f3", "r3i1p1f3", "r4i1p1f3", "r5i1p1f3"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f2","r2i1p1f2", "r3i1p1f2", "r4i1p1f2", "r5i1p1f2"],
        ]

ssp585_variant_id_list_of_lists=[
        ["r1i1p1f1", "r1i1p2f1", "r2i1p1f1", "r2i1p2f1", "r3i1p1f1", "r3i1p2f1", "r4i1p1f1", "r4i1p2f1",  "r5i1p1f1", "r5i1p2f1", "r6i1p1f1", "r6i1p2f1", "r7i1p2f1", "r8i1p1f1", "r8i1p2f1", "r9i1p1f1", "r9i1p2f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        [],
        ["r1i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f3","r2i1p1f3", "r3i1p1f3", "r4i1p1f3"],
        ["r1i1p1f1","r2i1p1f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        ["r1i1p1f1"],
        [],
        ]

data_path="/home/jonathan/Documents/Data_Improved/"
save_location="/home/jonathan/Documents/Figures/Future/scenario_combined_All_Variables_Annual/"

for i in range(0,1):
    var_name =VariableArray[i]
    title_name=TitleArray[i]
    plt.close()
    fig,axs=plt.subplots(1,1,sharex=True,gridspec_kw={'hspace': 0},figsize=(8,6))
    for k in range(0,1):
        source_plot(institution_id_list[k],source_id_list[k],control_expt_list[k],control_variant_list[k],hist_variant_id_list_of_lists[k],ssp119_variant_id_list_of_lists[k],ssp126_variant_id_list_of_lists[k],ssp245_variant_id_list_of_lists[k],ssp585_variant_id_list_of_lists[k],var_name,k,len(institution_id_list))
    plt.xticks(np.array([1850,1880,1910,1940,1970,2000,2030,2060,2090]),["1850","1880","1910","1940","1970","2000","2030","2060","2090"])
    plt.xlabel("time/years")
    plt.xlabel("time/years")
    plt.ylabel(title_name)
    plt.savefig(save_location+var_name+"_Scenario_Separate_Stacked_variability.pdf",dpi=300)
     
