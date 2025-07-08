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
from matplotlib.lines import Line2D



def run_avg(array,period):
    data_run_avg=np.zeros((np.shape(array)[0]-period))
    for j in range(0,np.shape(array)[0]-period):
        data_run_avg[j]=np.mean(array[j:j+period])
    return data_run_avg

def var_load(expt_id,variant_id,var_name):
    source_id="HadGEM3-GC31-LL"
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




institution_id="MOHC"
source_id="HadGEM3-GC31-LL"


ExptArray=["1pctCO2","abrupt-4xCO2"]
VariantArray=["r1i1p1f1", "r2i1p1f1", "r3i1p1f1", "r4i1p1f1"]







VariableArray=["acc", "rsiarea", "sst_thetao", "weddellgyre", "rossgyre", "siarea", "wsiarea", "ewmax", "ewpos", "maccpos", "naccpos", "saccpos", "wwmax", "wwpos","avgmld","w_avgmld","w_maxmld","maxmld","r_maxmld","a_maxmld","r_avgmld","hflux", "whflux", "rhflux", "uppercircrhon2", "lowercircrhon2"]

TitleArray=["ACC/Sv", "Ross Sea Ice Area/m", "Sea Surface Temperature \n south of 50S/K", "Weddell Gyre Strength/Sv", "Ross Gyre Strength/Sv", "Southern Ocean Sea Ice Area/m", "Weddell Sea Icea Area/m", "Easterly Wind Max Strength", "Position of Easterly Wind Maximum", "Latitude of the centre of the ACC", "Latitude of the northern edge of the ACC", "Latitude of the southern edge of the ACC", "Westerly Wind Max Strength", "Position of the Westerly Wind Maximum","Average Mixed Layer Depth \n south of 50S/m","Weddell Sea Mean Mixed layer Depth/m","Weddell Sea Max Mixed Layer Depth/m","Maximum Mixed Layer Depth \n south of 50S/m","Ross Sea Max Mixed Layer Depth/m","Arctic Max Mixed Layer Depth/m","Average Mixed Layer Depth in the Ross sea/m","Surface Heat Flux into the Ocean south of 50S/W","Surface Heat Flux into the Weddell Sea/W", "Surface Heat Flux into the Ross Sea/W", "Upper Meridional Circulation Strength/Sv","Lower Meridional Circulation Strength/Sv"]


#VariableArray=["htotal", "h65s", "h50s", "hequat20", "hweddellregion", "hrossregion", "h60s", "h40s", "h30s", "sst_thetaogloavg", "whflux", "rhflux", "hflux"]

#TitleArray=["Total Ocean heat", "Ocean heat south of 65S", "Ocean Heat South of 50S", "Heat 20 degrees either side of the equator", "Heat in the Weddell Sea", "Heat in the Ross Sea", "Heat South of 60S", "Heat South of 40S", "Heat South of 30S", "Global Mean SST", "Weddell Sea Heat Flux", "Ross Sea Heat Flux","Heat Flux below 50S"]

#VariableArray=["lowercircrhon2","uppercircrhon2"]

#TitleArray=["lowercircrhon2","uppercircrhon"]

#VariableArray=["r_avgmld"]
#TitleArray=["Average Mixed Layer Depth in the Ross sea/m"]

VariableArray=["acc", "avgdensity65", "avgdensity40s50s", "wwmax"]
TitleArray=["ACC/Sv", "Average Ocean Density South of 65$^{\circ}$S",  "Average Ocean Density 40-50$^{\circ}$S","Westerly Wind Max Strength/(Nm$^{-2}$)"]

VariableArray=["acc","avgmldd0","lowercircrhon2"]
TitleArray=["ACC/Sv","Average MLD south of 50$^{\circ}$S/m","Lower Circulation Strength/(kg/s)"]

VariableArray=["acc","maxmldd0","lowercircrhon2"]
TitleArray=["ACC/Sv","Maximum MLD south of 50$^{\circ}$S/m","Lower Circulation Strength/(kg/s)"]



#VariableArray=["avgmldd0", "maxmldd0", "r_maxmldd0", "r_avgmldd0", "w_maxmldd0", "w_avgmldd0"]
#TitleArray=["avgmldd0", "maxmldd0", "r_maxmldd0", "r_avgmldd0", "w_maxmldd0", "w_avgmldd0"]


#VariableArray=["acc","siarea","avgmldd0","maxmldd0","w_avgmldd0","r_avgmldd0","lowercircrhon2","uppercircrhon2","weddellgyre","weddellgyreuo","rossgyre","rossgyreuo"]
#TitleArray=["acc","siarea","avgmldd0","maxmldd0","w_avgmldd0","r_avgmldd0","lowercircrhon2","uppercircrhon2","weddellgyre","weddellgyreuo","rossgyre","rossgyreuo"]

#VariableArray=["acc","avgmldd0","lowercircrhon2","wwmax","avgdensitydiff","avgdensity40s50s","avgdensity65"]
#TitleArray=["ACC/Sv","Average MLD south of 50$^{\circ}$S","Lower Circulation Strength/(kg/s)","Max Westerly Wind Stress/(Nm$^{-2}$)","Average Density Difference \nacross the ACC/(kgm$^{-3}$)","Average Density Difference 40-50$^{\circ}$S/(kgm$^{-3}$)","Average Density Difference south of 65$^{\circ}$S/(kgm$^{-3}$)"]

rpa="R"

figure_labels=["(a)","(b)","(c)"]
data_path="/home/jonathan/Documents/Data_Improved/"
old_data_path="/home/jonathan/Documents/Data/"
save_location="/home/jonathan/Documents/Figures/Future/Met_Office_Warming_Runs_Stacked_Annual/"
control_indices=np.arange(1850,3850,1)
indices={}
indices["2850"]=np.arange(2850,3001,1)
indices["2937"]=np.arange(2937,3088,1)
indices["2991"]=np.arange(2991,3142,1)
indices["3044"]=np.arange(3044,3195,1)
index_names=["2850","2937","2991","3044"]
index_titles=["2850 (high)","2937 (low)","2991 (high)","3044 (low"]
#colours1pctCO2=["sandybrown","chocolate","orange","peru","darkorange"]
#colours4xCO2=["lightcoral","indianred","tomato","coral","red"]
#colours1pctCO2=["cyan","royalblue","forestgreen","lime","blue"]
#colours4xCO2=["tomato","darkorange","hotpink","saddlebrown","red"]
colours=["tomato","cyan","darkorange","royalblue"]
custom_lines = [Line2D([0], [0], color="tomato", lw=2),
                Line2D([0], [0], color="cyan", lw=2),
                Line2D([0], [0], color="darkorange", lw=2),
                Line2D([0], [0], color="royalblue", lw=2),
                Line2D([0], [0], color="k", lw=2),
                Line2D([0], [0], color="k", lw=2),
                Line2D([0], [0], color="k", lw=2,linestyle="dashed")]

plt.close()
fig,axs=plt.subplots(len(VariableArray),sharex=True,gridspec_kw={'hspace': 0},figsize=(8,8))
for i in range(0,len(VariableArray)):
    expt_id="piControl"
    variant_id="r1i1p1f1"
    var_name =VariableArray[i]
    title_name=TitleArray[i]
    if var_name=="avgmldd0":
        control_values=var_load(expt_id,variant_id,var_name)
        control_values[np.where(control_values<0)]=control_values[np.where(control_values<0)]*-1
        axs[i].boxplot(control_values[850:1350],positions=[-5],widths=5,whis=(0,100))
    elif var_name=="avgdensitydiff":
        control_values=var_load(expt_id,variant_id,"avgdensity65")-var_load(expt_id,variant_id,"avgdensity40s50s")
        axs[i].boxplot(control_values[850:1350],positions=[-5],widths=5,whis=(0,100))
    else:
        control_values=var_load(expt_id,variant_id,var_name)
        axs[i].boxplot(control_values[850:1350],positions=[-5],widths=5,whis=(0,100))
    axs[i].set_ylabel(title_name)
    axs[-1].set_xlabel("Time/years")

    for j in range(0,len(ExptArray)):
        expt_id=ExptArray[j]
        data=[]
        max_len=0
        if j==0:
            for k in range(0,len(VariantArray)):
                try:
                    variant_id=VariantArray[k]
                    if var_name!="avgdensitydiff" and var_name!="avgmldd0":
                        var_data=run_avg(var_load(expt_id,variant_id,var_name),10)
                    elif var_name=="avgdensitydiff":
                        var_data=run_avg(var_load(expt_id,variant_id,"avgdensity65"),10)-run_avg(var_load(expt_id,variant_id,"avgdensity40s50s"),10)
                    elif var_name=="avgmldd0":
                        var_data=var_load(expt_id,variant_id,var_name)
                        var_data[np.where(var_data<0)]=var_data[np.where(var_data<0)]
                        var_data=run_avg(var_data,10)
                    data.append(var_data)
                    max_len=np.nanmax((len(var_data),max_len))
                    if index_names[k]=="2850" or index_names[k]=="2991":
                        axs[i].plot(var_data,label=index_titles[k],color=colours[k],alpha=0.55,linestyle="dashed")
                    else:
                        axs[i].plot(var_data,label=index_titles[k],color=colours[k],alpha=0.55,linestyle="dashed")
                except:
                    print("Failed "+expt_id+variant_id)
            data_array=np.zeros((len(data),max_len))
            data_array.fill(np.nan)
            for l in range(0,len(data)):
                length=len(data[l])
                data_array[l,:length]=data[l]
            axs[i].plot(np.nanmean(data_array,axis=0),color="k",linestyle="dashed")

        elif j==1:
            for k in range(0,len(VariantArray)):
                try:
                    if k==0:
                        index_index=3
                    elif k==1:
                        index_index=0
                    elif k==2:
                        index_index=1
                    elif k==3:
                        index_index=2
                    variant_id=VariantArray[index_index]
                    if var_name!="avgdensitydiff":
                        var_data=run_avg(var_load(expt_id,variant_id,var_name),10)
                    else:
                        var_data=run_avg(var_load(expt_id,variant_id,"avgdensity65"),10)-run_avg(var_load(expt_id,variant_id,"avgdensity40s50s"),10)
                    data.append(var_data)
                    max_len=np.nanmax((len(var_data),max_len))
                    if index_names[k]=="2850" or index_names[k]=="2991":
                        axs[i].plot(var_data,label=index_titles[k],color=colours[k],alpha=0.55)
                    else:
                        axs[i].plot(var_data,label=index_titles[k],color=colours[k],alpha=0.55)
                except:
                    print("Failed "+expt_id+variant_id)
            data_array=np.zeros((len(data),max_len))
            data_array.fill(np.nan)
            for j in range(0,len(data)):
                length=len(data[j])
                data_array[j,:length]=data[j]
            axs[i].plot(np.nanmean(data_array,axis=0),color="k")
    axs[i].set_xticks(ticks=(0,20,40,60,80,100,120,140))
    axs[i].set_xlim(-10,140)
    axs[-1].legend(custom_lines,["2850 (high)","2937 (low)","2991 (high)","3044 (low)","mean","4xCO2","1pctCO2"],ncol=2)
    axs[i].grid(visible=True,which="major")
    at=AnchoredText(figure_labels[i],prop=dict(size=12),frameon=False,loc='upper right')
    axs[i].add_artist(at)
    plt.tight_layout()
plt.xticks(ticks=(0,20,40,60,80,100,120,140),labels=(0,20,40,60,80,100,120,140))
plt.savefig(save_location+"Forcing_Paper_Decadal_Warming_Stacked_NewLegend_maxmld.pdf")


