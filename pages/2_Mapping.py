
import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import geopandas as gpd
import os
import zipfile
from pmdarima import auto_arima

from sklearn.metrics import r2_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import confusion_matrix, accuracy_score
import sklearn.metrics as metrics

# data reading/cleaning 
zf1 = zipfile.ZipFile('./projects/pollution/Korea.zip') 
pollution = pd.read_csv(zf1.open('Measurement_summary.csv'))
zf2 = zipfile.ZipFile('./projects/pollution/Seoul.zip') 
Seoul = pd.read_csv(zf2.open('Measurement_summary.csv'))
Seoulmod = Seoul.copy()
Seoulmod["Measurement date"]=Seoulmod["Measurement date"].str.slice(0,4)
Seoulmod["Address"]=Seoulmod["Address"].str.split(',').str[2].str.strip()
Seoulmod2017=Seoulmod[Seoulmod["Measurement date"]=="2017"].groupby(["Station code","Address","Latitude","Longitude"]).mean().reset_index()
Seoulmod2018=Seoulmod[Seoulmod["Measurement date"]=="2018"].groupby(["Station code","Address","Latitude","Longitude"]).mean().reset_index()
Seoulmod2019=Seoulmod[Seoulmod["Measurement date"]=="2019"].groupby(["Station code","Address","Latitude","Longitude"]).mean().reset_index()
tempSeoulGep=gpd.read_file("./projects/pollution/seoul_municipalities_geo.json")
SeoulGeo_pollution2017= tempSeoulGep.merge(Seoulmod2017, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)
SeoulGeo_pollution2018= tempSeoulGep.merge(Seoulmod2018, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)
SeoulGeo_pollution2019= tempSeoulGep.merge(Seoulmod2019, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)


f, axes = plt.subplots(figsize=(10, 5), ncols=3, nrows=2,layout="compressed")
SeoulGeo_pollution2017.plot(ax=axes[0][0], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"})
SeoulGeo_pollution2017.plot(ax=axes[0][1], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"})
SeoulGeo_pollution2017.plot(ax=axes[0][2], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"})
SeoulGeo_pollution2019.plot(ax=axes[1][0], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"})
SeoulGeo_pollution2019.plot(ax=axes[1][1], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"})
SeoulGeo_pollution2019.plot(ax=axes[1][2], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"})
for i, ax_row in enumerate(axes):
    for j, ax in enumerate(ax_row):
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Set title for the first column in each row
        if j == 1:
            ax.set_title("2017" if i == 0 else "2019", fontsize=16)

st.pyplot(f)


test = pd.DataFrame(pollution)
st.dataframe(pollution)