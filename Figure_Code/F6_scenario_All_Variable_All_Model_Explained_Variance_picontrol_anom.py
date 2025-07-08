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
from sklearn import linear_model
from sklearn.metrics import explained_variance_score


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
    elif var_name=="acc":
        var_name="accuo"
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


#VariableArray=["acc", "rsiarea", "sst_thetao", "weddellgyre", "rossgyre", "siarea", "wsiarea", "ewmax", "ewpos", "maccpos", "naccpos", "saccpos", "wwmax", "wwpos","avgmld","w_avgmld","w_maxmld","maxmld","r_maxmld","a_maxmld"]

#TitleArray=["acc", "rsiarea", "sst_thetao", "weddellgyre", "rossgyre", "siarea", "wsiarea", "ewmax", "ewpos", "maccpos", "naccpos", "saccpos", "wwmax", "wwpos","avgmld","w_avgmld","w_maxmld","maxmld","r_maxmld","a_maxmld"]


#VariableArray=["lowercircrhon2","uppercircrhon2"]

#TitleArray=["lowercircrhon2","uppercircrhon"]


#VariableArray=["whflux","rhflux","hflux"]
#TitleArray=["Weddell Heat Flux", "Ross Heat Flux", "Heat Flux south of 50S"]

#VariableArray=["r_avgmldd0", "avgmldd0", "w_maxmldd0", "w_avgmldd0", "r_maxmldd0", "maxmldd0", "l_maxmldd0", "a_maxmldd0", "siarea"]
#TitleArray=["Ross mean mld", "Mean mld south of 50S", "Weddell max mld", "Weddel mean mld", "Ross max mld", "Max mld south of 50S", "Labrador max mld", "Arctic max mld", "Sea Ice Area"]


VariableArray=["acc","siarea","avgmldd0","maxmldd0","w_avgmldd0","r_avgmldd0","lowercircrhon2","uppercircrhon2","weddellgyre","weddellgyreuo","rossgyre","rossgyreuo"]
TitleArray=["acc","siarea","avgmldd0","maxmldd0","w_avgmldd0","r_avgmldd0","lowercircrhon2","uppercircrhon2","weddellgyre","weddellgyreuo","rossgyre","rossgyreuo"]

VariableArray=["acc","maxmldd0","lowercircrhon2","lowercircrhon2uo"]
TitleArray=["ACC/Sv","maxmldd0","lowercircrhon2","lowercircrhon2uo"]

rpa="R"
institution_id_list=[
    "CCCma",
    "CSIRO-ARCCSS",
    "EC-Earth-Consortium",
    "MOHC",
    "IPSL",
    "MIROC",
    "MOHC"
    ]
source_id_list=[
    "CanESM5",
    "ACCESS-CM2",
    "EC-Earth3",
    "HadGEM3-GC31-LL",
    "IPSL-CM6A-LR",
    "MIROC6",
    "UKESM1-0-LL"
    ]
control_expt_list=[
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
        "r1i1p1f2"
        ]
hist_variant_id_list_of_lists=[
        ["r1i1p1f1", "r1i1p2f1", "r2i1p1f1", "r2i1p2f1", "r3i1p1f1", "r3i1p2f1", "r4i1p1f1", "r4i1p2f1",  "r5i1p1f1", "r5i1p2f1", "r6i1p1f1", "r6i1p2f1", "r7i1p1f1", "r7i1p2f1", "r8i1p1f1", "r8i1p2f1", "r9i1p1f1", "r9i1p2f1", "r10i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f3","r5i1p1f3","r11i1p1f3","r25i1p1f3"],
        ["r1i1p1f1", "r2i1p1f1", "r3i1p1f1", "r4i1p1f1", "r5i1p1f1", "r6i1p1f1", "r7i1p1f1", "r8i1p1f1", "r9i1p1f1"],
        ["r1i1p1f1", "r2i1p1f1", "r3i1p1f1", "r4i1p1f1", "r5i1p1f1"],
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
        ]

ssp126_variant_id_list_of_lists=[
        ["r1i1p1f1", "r1i1p2f1", "r2i1p1f1", "r2i1p2f1", "r3i1p1f1", "r3i1p2f1", "r4i1p1f1", "r4i1p2f1",  "r5i1p1f1", "r5i1p2f1", "r6i1p1f1", "r6i1p2f1", "r7i1p1f1", "r7i1p2f1", "r8i1p1f1", "r8i1p2f1", "r9i1p1f1", "r9i1p2f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        [],
        ["r1i1p1f2","r2i1p1f2", "r3i1p1f2", "r4i1p1f2", "r5i1p1f2"],
        ]

ssp245_variant_id_list_of_lists=[
        ["r1i1p1f1","r3i1p1f1","r3i1p2f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        ["r1i1p1f1","r2i1p1f1"],
        ["r1i1p1f3","r2i1p1f3", "r3i1p1f3", "r4i1p1f3", "r5i1p1f3"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        ["r1i1p1f2","r2i1p1f2", "r3i1p1f2", "r4i1p1f2", "r5i1p1f2"],
        ]

ssp585_variant_id_list_of_lists=[
        ["r1i1p1f1", "r1i1p2f1", "r2i1p1f1", "r2i1p2f1", "r3i1p1f1", "r3i1p2f1", "r4i1p1f1", "r4i1p2f1",  "r5i1p1f1", "r5i1p2f1", "r6i1p1f1", "r6i1p2f1", "r7i1p2f1", "r8i1p1f1", "r8i1p2f1", "r9i1p1f1", "r9i1p2f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        ["r1i1p1f1"],
        ["r1i1p1f3","r2i1p1f3", "r3i1p1f3", "r4i1p1f3"],
        ["r1i1p1f1","r2i1p1f1"],
        ["r1i1p1f1","r2i1p1f1", "r3i1p1f1"],
        [],
        ]

data_path="/home/jonathan/Documents/Data_Improved/"
save_location="/home/jonathan/Documents/Figures/Future/scenario_combined_Explained_Variance/"

for i in range(0,1):
    var_name =VariableArray[i]
    title_name=TitleArray[i]
    plt.close()
    fig,axs=plt.subplots(3,sharex=True,gridspec_kw={'hspace': 0,'wspace':0},figsize=(7,7))
    init_mean_state=[]
    forcings=[]
    min_len=300
    data=[]
    for k in range(0,len(institution_id_list)):
        institution_id,source_id,control_expt_id,control_variant_id,variant_list,ssp119_variant_list,ssp126_variant_list,ssp245_variant_list,ssp585_variant_list,var_name,loc_index,institution_number=institution_id_list[k],source_id_list[k],control_expt_list[k],control_variant_list[k],hist_variant_id_list_of_lists[k],ssp119_variant_id_list_of_lists[k],ssp126_variant_id_list_of_lists[k],ssp245_variant_id_list_of_lists[k],ssp585_variant_id_list_of_lists[k],var_name,k,len(institution_id_list)
        init_mean_state_val=np.nanmean(var_load(source_id,control_expt_id,control_variant_id,var_name))
        
        expt_id="ssp119"
        for j in range(0,len(ssp119_variant_list)):
            variant_id=ssp119_variant_list[j]
            try:
                if var_name=="acc":
                    try:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                    except:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,"accuo"),10)
                else:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                if np.nanmean(var_data)<0:
                    var_data=-var_data
                if var_name=="acc" and np.nanmean(var_data)<0.5:
                    var_data=var_data*1000
                if np.nanmean(var_data)!=0 and len(var_data)>50:
                    data.append(var_data)
                    min_len=np.nanmin((len(var_data),min_len))
                    model_force=np.zeros(len(source_id_list))
                    model_force[k]=1
                    forcings.append(np.append(np.array((1,0,0,0)),model_force))
                    init_mean_state.append(init_mean_state_val)
                    print(k,j,len(data),len(forcings))
            except:
                print(institution_id,source_id,expt_id,variant_id,var_name,"failed")

        expt_id="ssp126"
        for j in range(0,len(ssp126_variant_list)):
            variant_id=ssp126_variant_list[j]
            try:
                if var_name=="acc":
                    try:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                    except:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,"accuo"),10)
                else:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                if np.nanmean(var_data)<0:
                    var_data=-var_data
                if var_name=="acc" and np.nanmean(var_data)<0.5:
                    var_data=var_data*1000
                if np.nanmean(var_data)!=0 and len(var_data)>50:
                    data.append(var_data)
                    min_len=np.nanmin((len(var_data),min_len))
                    model_force=np.zeros(len(source_id_list))
                    model_force[k]=1
                    forcings.append(np.append(np.array((0,1,0,0)),model_force))
                    init_mean_state.append(init_mean_state_val)
                    print(k,j,len(data),len(forcings))
            except:
                print(institution_id,source_id,expt_id,variant_id,var_name,"failed")
        expt_id="ssp245"
        for j in range(0,len(ssp245_variant_list)):
            variant_id=ssp245_variant_list[j]
            try:
                if var_name=="acc":
                    try:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                    except:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,"accuo"),10)
                else:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                if np.nanmean(var_data)<0:
                    var_data=-var_data
                if var_name=="acc" and np.nanmean(var_data)<0.5:
                    var_data=var_data*1000
                if np.nanmean(var_data)!=0 and len(var_data)>50:
                    data.append(var_data)
                    min_len=np.nanmin((len(var_data),min_len))
                    model_force=np.zeros(len(source_id_list))
                    model_force[k]=1
                    forcings.append(np.append(np.array((0,0,1,0)),model_force))
                    init_mean_state.append(init_mean_state_val)
                    print(k,j,len(data),len(forcings))
            except:
                print(institution_id,source_id,expt_id,variant_id,var_name,"failed")
        expt_id="ssp585"
        for j in range(0,len(ssp585_variant_list)):
            variant_id=ssp585_variant_list[j]
            try:
                if var_name=="acc":
                    try:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                    except:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,"accuo"),10)
                else:
                        var_data=run_avg(var_load(source_id,expt_id,variant_id,var_name),10)
                if np.nanmean(var_data)<0:
                    var_data=-var_data
                if var_name=="acc" and np.nanmean(var_data)<0.5:
                    var_data=var_data*1000

                if np.nanmean(var_data)!=0 and len(var_data)>50:
                    data.append(var_data)
                    min_len=np.nanmin((len(var_data),min_len))
                    model_force=np.zeros(len(source_id_list))
                    model_force[k]=1
                    forcings.append(np.append(np.array((0,0,0,1)),model_force))
                    init_mean_state.append(init_mean_state_val)
                    print(k,j,len(data),len(forcings))
            except:
                print(institution_id,source_id,expt_id,variant_id,var_name,"failed")





    full_data=data
    x=np.arange(2015,2015+min_len-1)
    data_array=np.zeros((len(full_data),min_len))
    print(min_len)
    for j in range(0,len(full_data)):
        data_array[j,:]=full_data[j][:min_len]
    init_value_array=np.tile(np.reshape(data_array[:,0],(len(full_data),1)),(1,min_len))
    anomaly_data_array=data_array-init_value_array
    predictors=np.zeros((len(full_data),5+len(source_id_list)))
    predictors[:,0]=data_array[:,0]
    predictors[:,1:]=forcings
    explained_variance_model=np.zeros((min_len))
    explained_variance_init=np.zeros((min_len))
    explained_variance_full=np.zeros((min_len))
    for j in range(0,min_len):
        model_regr=linear_model.LinearRegression()
        model_regr.fit(predictors[:,5:].reshape((len(full_data),len(source_id_list))),anomaly_data_array[:,j].reshape((len(full_data))))
        model_pred=model_regr.predict(predictors[:,5:].reshape((len(full_data),len(source_id_list))))
        explained_variance_model[j]=explained_variance_score(anomaly_data_array[:,j],model_pred)
        init_regr=linear_model.LinearRegression()
        init_regr.fit(predictors[:,1:].reshape((len(full_data),len(source_id_list)+4)),anomaly_data_array[:,j].reshape((len(full_data))))
        init_pred=init_regr.predict(predictors[:,1:].reshape((len(full_data),len(source_id_list)+4)))
        explained_variance_init[j]=explained_variance_score(anomaly_data_array[:,j],init_pred)
        full_regr=linear_model.LinearRegression()
        full_regr.fit(predictors,anomaly_data_array[:,j])
        full_pred=full_regr.predict(predictors)
        explained_variance_full[j]=explained_variance_score(anomaly_data_array[:,j],full_pred)
    axs[1].fill_between(x,0,explained_variance_model[1:],color="y",label="Model")
    axs[1].fill_between(x,explained_variance_model[1:],explained_variance_init[1:],color="r",label="Forced")
    axs[1].fill_between(x,explained_variance_init[1:],explained_variance_full[1:],color="b",label="Initial Conditions")
    axs[1].fill_between(x,explained_variance_full[1:],1,color="grey",label="Internal Variability")
    predictors=np.zeros((len(full_data),5+len(source_id_list)))
    predictors[:,0]=data_array[:,0]
    predictors[:,1:]=forcings
    explained_variance_model=np.zeros((min_len))
    explained_variance_init=np.zeros((min_len))
    explained_variance_full=np.zeros((min_len))
    for j in range(0,min_len):
        model_regr=linear_model.LinearRegression()
        model_regr.fit(predictors[:,5:].reshape((len(full_data),len(source_id_list))),data_array[:,j].reshape((len(full_data))))
        model_pred=model_regr.predict(predictors[:,5:].reshape((len(full_data),len(source_id_list))))
        explained_variance_model[j]=explained_variance_score(data_array[:,j],model_pred)
        init_regr=linear_model.LinearRegression()
        init_regr.fit(predictors[:,1:].reshape((len(full_data),len(source_id_list)+4)),data_array[:,j].reshape((len(full_data))))
        init_pred=init_regr.predict(predictors[:,1:].reshape((len(full_data),len(source_id_list)+4)))
        explained_variance_init[j]=explained_variance_score(data_array[:,j],init_pred)
        full_regr=linear_model.LinearRegression()
        full_regr.fit(predictors,data_array[:,j])
        full_pred=full_regr.predict(predictors)
        explained_variance_full[j]=explained_variance_score(data_array[:,j],full_pred)
    axs[0].fill_between(x,0,explained_variance_model[1:],color="y",label="Model")
    axs[0].fill_between(x,explained_variance_model[1:],explained_variance_init[1:],color="r",label="Forced")
    axs[0].fill_between(x,explained_variance_init[1:],explained_variance_full[1:],color="b",label="Initial Conditions")
    axs[0].fill_between(x,explained_variance_full[1:],1,color="grey",label="Internal Variability")



    picontrol_mean_array=np.tile(np.reshape(init_mean_state,(len(full_data),1)),(1,min_len))
    anomaly_data_array=data_array-picontrol_mean_array
    predictors=np.zeros((len(full_data),5+len(source_id_list)))
    predictors[:,0]=data_array[:,0]-init_mean_state
    predictors[:,1:]=forcings
    explained_variance_model=np.zeros((min_len))
    explained_variance_init=np.zeros((min_len))
    explained_variance_full=np.zeros((min_len))
    for j in range(0,min_len):
        model_regr=linear_model.LinearRegression()
        model_regr.fit(predictors[:,5:].reshape((len(full_data),len(source_id_list))),anomaly_data_array[:,j].reshape((len(full_data))))
        model_pred=model_regr.predict(predictors[:,5:].reshape((len(full_data),len(source_id_list))))
        explained_variance_model[j]=explained_variance_score(anomaly_data_array[:,j],model_pred)
        init_regr=linear_model.LinearRegression()
        init_regr.fit(predictors[:,1:].reshape((len(full_data),len(source_id_list)+4)),anomaly_data_array[:,j].reshape((len(full_data))))
        init_pred=init_regr.predict(predictors[:,1:].reshape((len(full_data),len(source_id_list)+4)))
        explained_variance_init[j]=explained_variance_score(anomaly_data_array[:,j],init_pred)
        full_regr=linear_model.LinearRegression()
        full_regr.fit(predictors,anomaly_data_array[:,j])
        full_pred=full_regr.predict(predictors)
        explained_variance_full[j]=explained_variance_score(anomaly_data_array[:,j],full_pred)
    axs[2].fill_between(x,0,explained_variance_model[1:],color="y",label="Model")
    axs[2].fill_between(x,explained_variance_model[1:],explained_variance_init[1:],color="r",label="Forced")
    axs[2].fill_between(x,explained_variance_init[1:],explained_variance_full[1:],color="b",label="Initial Conditions")
    axs[2].fill_between(x,explained_variance_full[1:],1,color="grey",label="Internal Variability")






    axs[0].legend(loc="lower right")
    axs[1].legend(loc="lower right")
    axs[2].legend(loc="lower right")
    axs[0].set_ylabel("Raw Data \n Explained Fraction of Variance",rotation=75,labelpad=30)
    axs[1].set_ylabel("Initial Value Anomaly \n Explained Fraction of Variance",rotation=75,labelpad=30)
    axs[2].set_ylabel("PiControl Mean State Anomaly \n Explained Fraction of Variance",rotation=75,labelpad=30)
    axs[2].set_xlabel("time/years")
    at=AnchoredText("(a)",prop=dict(size=12),frameon=False,loc='upper left')
    axs[0].add_artist(at)
    at=AnchoredText("(b)",prop=dict(size=12),frameon=False,loc='upper left')
    axs[1].add_artist(at)
    at=AnchoredText("(c)",prop=dict(size=12),frameon=False,loc='upper left')
    axs[2].add_artist(at)




    axs[0].set_title(title_name)
    plt.tight_layout()
    plt.savefig(save_location+var_name+"_Scenario_Explained_Variance_Full_Model_Mean_State.pdf",dpi=300)
     
