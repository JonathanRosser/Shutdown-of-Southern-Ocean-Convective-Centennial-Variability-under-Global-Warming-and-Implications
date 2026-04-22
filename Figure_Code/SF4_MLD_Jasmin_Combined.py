import xarray as xr
import numpy as np
import sys
sys.path.append('/home/users/jonros74/Coding/')
from JonTools import jon_data
from JonTools import latlon
import datetime
import os
import matplotlib.pyplot as plt
import matplotlib
import traceback

#Loop through relevant models
InstitutionArray=["BCC","CCCma", "CNRM-CERFACS", "CSIRO", "CSIRO-ARCCSS", "EC-Earth-Consortium", "IPSL", "MIROC", "MIROC", "MPI-M", "MRI", "NASA-GISS", "NCC", "NOAA-GFDL","MOHC","MOHC"]

SourceArray=["BCC-ESM1", "CanESM5", "CNRM-ESM2-1", "ACCESS-ESM1-5", "ACCESS-CM2", "EC-Earth3", "IPSL-CM6A-LR", "MIROC6", "MIROC-ES2L", "MPI-ESM1-2-HR", "MRI-ESM2-0", "GISS-E2-1-G", "NorESM2-MM", "GFDL-CM4","UKESM1-0-LL","HadGEM3-GC31-LL"]

ExptArray=["piControl", "esm-piControl", "esm-piControl", "esm-piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl", "piControl","piControl", "piControl"]

VariantArray=["r1i1p1f1", "r1i1p1f1", "r1i1p1f2", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f2", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1", "r1i1p1f1","r1i1p1f2", "r1i1p1f1"]

freq="mon"
spatial="glo"


fig,axs=plt.subplots(nrows=4,ncols=4,sharex=True,sharey=True,figsize=(8,8),gridspec_kw={'hspace': 0.08,'wspace':0.05})
for i in range(0,len(InstitutionArray)):
        try:
            Institution=InstitutionArray[i]
            Source=SourceArray[i]
            Expt=ExptArray[i]
            Variant=VariantArray[i]
            print(Source)
            rpa="R"
            source_name=Source+"_"+Expt+"_"+Variant+"_"	
            filename="/gws/ssde/j25a/orchestra/vol2/jonros74/Data/"+Source+"/"+Expt+"/"+Variant+"/"+rpa+"/mld003/mld003_"+rpa+"_"+freq+"_"+spatial+"_"+source_name+"*.nc"
            MLD003_array=xr.open_mfdataset(filename)
            #MLD003_array=xr.open_dataset("/gws/nopw/j04/orchestra_vol2/jonros74/Data/"+Source+"/"+Expt+"/"+Variant+"/"+rpa+"/mld003/mld003_"+rpa+"_"+freq+"_"+spatial+"_"+source_name+"*.nc")
            mld_values=MLD003_array.mld003[:120].values
            thetao_array=jon_data.cmip6_load(Institution,Source,Expt,Variant,"Omon","thetao")
            area_mask=latlon.area(thetao_array,maxlat=-50)
            draw_mask=latlon.area(thetao_array,maxlat=-40,minlat=-80)
            max_j_index=np.nanmax(np.where(draw_mask==1)[0])
            min_j_index=np.nanmin(np.where(draw_mask==1)[0])
            latitude=jon_data.coord_get(thetao_array,"latitude")
            longitude=jon_data.coord_get(thetao_array,"longitude")
            if latitude.ndim==2:
                mean_latitude=np.nanmean(latitude,axis=-1)
            elif latitude.ndim==1:
                mean_latitude=latitude
            elif latitude.ndim==3:
                mean_latitude=np.nanmean(latitude,axis=(0,2))
            if longitude.ndim==2:
                mean_longitude=longitude[int(max_j_index/2),:]
            elif longitude.ndim==1:
                mean_longitude=longitude
            elif longitude.ndim==3:
                mean_longitude=np.nanmean(longitude[:,int(max_j_index/2),:],axis=(0))
            lon_shift=np.where(mean_longitude==np.min(mean_longitude))[0][0]
            rolled_longitude=np.roll(mean_longitude,shift=-lon_shift)
            rolled_mld_values=np.roll(mld_values,shift=-lon_shift,axis=2)
            #msftbarot_values=np.roll(jon_data.cmip6_load(Institution,Source,Expt,Variant,"Omon","msftbarot").get("msftbarot")[:,:max_j_index,:].mean(dim="time").values,shift=-lon_shift,axis=1)
            row=np.mod(i,4)
            column=np.floor_divide(i,4)
            
            axs[row,column].pcolormesh(rolled_longitude,mean_latitude[min_j_index:max_j_index],np.nanmean(rolled_mld_values,axis=0)[min_j_index:max_j_index,:],shading="auto",rasterized=True)
            axs[row,column].set_xlim(-180,180)
            axs[row,column].set_ylim(-80,-40)
            #axs[row,column].set_title(Source,loc="center",y=1.0,pad=-18,color="orange")
            #axs[row,column].set_title(Source,loc="center",pad=-18,color="orange")
            #axs[row,column].contour(rolled_longitude,mean_latitude[:max_j_index],msftbarot_values,colors="orange",linewidths=0.5,linestyles="solid",levels=15)
            axs[row, column].text(
                0.5, 0.95, Source,
                transform=axs[row, column].transAxes,
                ha='center', va='top',
                color='orange',
                fontsize=9
            )

            axs[-1,column].set_xlabel("longitude")
            axs[row,0].set_ylabel("latitude")
            plt.suptitle("Average Mixed Layer")
        except:
            try:
                Institution=InstitutionArray[i]
                Source=SourceArray[i]
                Expt=ExptArray[i]
                Variant=VariantArray[i]
                print(Source)
                rpa="R"
                source_name=Source+"_"+Expt+"_"+Variant+"_"
                filename="/gws/ssde/j25a/orchestra/vol2/jonros74/Data/"+Source+"/"+Expt+"/"+Variant+"/"+rpa+"/mld003/"
                names=os.listdir(filename)
                mld_values=[]
                for name in names:
                    if len(mld_values)==0:
                        mld_values=xr.open_dataset(filename+name).mld003.values
                    else:
                        #mld_values=np.append(mld_values,xr.open_dataset(name).mld003.values,axis=0)
                        print(name)
                thetao_array=jon_data.cmip6_load(Institution,Source,Expt,Variant,"Omon","thetao")
                area_mask=latlon.area(thetao_array,maxlat=-50)
                draw_mask=latlon.area(thetao_array,maxlat=-40,minlat=-80)
                max_j_index=np.nanmax(np.where(draw_mask==1)[0])
                min_j_index=np.nanmin(np.where(draw_mask==1)[0])

                latitude=jon_data.coord_get(thetao_array,"latitude")
                longitude=jon_data.coord_get(thetao_array,"longitude")
                if latitude.ndim==2:
                    mean_latitude=np.nanmean(latitude,axis=-1)
                elif latitude.ndim==1:
                    mean_latitude=latitude
                elif latitude.ndim==3:
                    mean_latitude=np.nanmean(latitude,axis=(0,2))
                if longitude.ndim==2:
                    mean_longitude=longitude[int(max_j_index/2),:]
                elif longitude.ndim==1:
                    mean_longitude=longitude
                elif longitude.ndim==3:
                    mean_longitude=np.nanmean(longitude[:,int(max_j_index/2),:],axis=(0))
                lon_shift=np.where(mean_longitude==np.min(mean_longitude))[0][0]
                rolled_longitude=np.roll(mean_longitude,shift=-lon_shift)
                rolled_mld_values=np.roll(mld_values,shift=-lon_shift,axis=2)
                #msftbarot_values=np.roll(jon_data.cmip6_load(Institution,Source,Expt,Variant,"Omon","msftbarot").get("msftbarot")[:,:max_j_index,:].mean(dim="time").values,shift=-lon_shift,axis=1)
                row=np.mod(i,4)
                column=np.floor_divide(i,4)
                
                axs[row,column].pcolormesh(rolled_longitude,mean_latitude[min_j_index:max_j_index],np.nanmean(rolled_mld_values,axis=0)[min_j_index:max_j_index,:],shading="auto",rasterized=True)
                #axs[row,column].contour(rolled_longitude,mean_latitude[:max_j_index],msftbarot_values,colors="orange",linewidths=0.5,linestyles="solid",levels=15)
                axs[row,column].set_xlim(-180,180)
                axs[row,column].set_ylim(-80,-40)
                #if row!=3:
                #axs[row,column].set_title(Source,loc="center",y=1.0,pad=-18,color="orange")
                #axs[row,column].set_title(Source,loc="center",pad=-18,color="orange")
                #else:
                #	 axs[row,column].set_title(Source,loc="center",pad=-30,color="orange")
                axs[row, column].text(
                    0.5, 0.95, Source,
                    transform=axs[row, column].transAxes,
                    ha='center', va='top',
                    color='orange',
                    fontsize=9
                )


                axs[-1,column].set_xlabel("longitude")
                axs[row,0].set_ylabel("latitude")
                plt.suptitle("Average Mixed Layer of "+Source+"/m")


            except Exception as e:
                print(Source,"failed", e)
                traceback.print_exc()

norm = matplotlib.colors.Normalize(vmin=0,vmax=1)
cbar = fig.colorbar(
    matplotlib.cm.ScalarMappable(cmap="viridis", norm=norm), ax=axs, orientation='vertical', shrink=0.9, aspect=25, pad=0.02
)
cbar.set_label("MLD/(min to max)", fontsize=12)
cbar.ax.tick_params(labelsize=10)


plt.savefig("/gws/ssde/j25a/orchestra/vol1/jonros74/Figures/MLD_Plots/Combined/avgmld_Combined.pdf")

