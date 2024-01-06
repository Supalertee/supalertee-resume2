
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
from streamlit.hello.utils import show_code



st.markdown("# Seoul Pollution/ Time-series Forecasting")
st.markdown('''I start doing this small project to summarize and apply the knowledge of myself study in data science and machine learning. Eventhough most of\
    Data analysis and Data science focusing on basic of scikit-learn but in this data set I found that scikit-learn cannot predict well. The problem is because\
    I found that the pollution data is **_Periodic_**, which will be show soon, so that we need a time-series ML model to predict them. This problem tickle me\
    to gain some knowledge by doing this project since I have never use time-series ML before.''')

st.markdown("# Define Probelm")
st.markdown(''' As a foreigner who living in Korea for 3.5 years, I realize that every springs and some season, Seoul encouter with terrible pollution problem.\
    I would like to see the overall increasing and behavior of pollution in Seoul and find out what are the main causes of this probel (if it possible) .\
    In quantitative research sense, we will see how pollution in Seoul change over years and will find the correlation to other factor, weather, people's activities\
    and so-on. To answer the question **_How pollution in Seoul behave quantitatively and what are the causes?_**''')

st.markdown("# Data Collection")
st.markdown(''' Since pollution is the main problem nowadays, I can find very good sources of South Korea pollution data. So, I decided to select 2 dataset''')

def datareading():
    zf1 = zipfile.ZipFile('./projects/pollution/Korea.zip') 
    pollution = pd.read_csv(zf1.open('south-korean-pollution-data.csv'))
    zf2 = zipfile.ZipFile('./projects/pollution/Seoul.zip') 
    Seoul = pd.read_csv(zf2.open('Measurement_summary.csv'))
    return pollution,Seoul
show_code(datareading)

pollution,Seoul = datareading()
Seoulmod = Seoul.copy()
st.dataframe(Seoulmod)

# st.markdowm(''' We first normalize data for each column to simple ''')
# unlike in Jupiter .groupby('').mean() in streamlit is require one culumns. So, I decited to droup all important column
Seoulmod["Measurement date"]=Seoulmod["Measurement date"].str.slice(0,4)
Seoulmod["Address"]=Seoulmod["Address"].str.split(',').str[2].str.strip()
Seoulmod = Seoulmod.drop(["Latitude","Longitude","Station code"],axis=1)

Seoulmodoverall =Seoulmod.drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
Seoulmod2017=Seoulmod[Seoulmod["Measurement date"]=="2017"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
Seoulmod2018=Seoulmod[Seoulmod["Measurement date"]=="2018"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
Seoulmod2019=Seoulmod[Seoulmod["Measurement date"]=="2019"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
tempSeoulGep=gpd.read_file("./projects/pollution/seoul_municipalities_geo.json")
SeoulGeo_pollution2017= tempSeoulGep.merge(Seoulmod2017, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)
SeoulGeo_pollution2018= tempSeoulGep.merge(Seoulmod2018, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)
SeoulGeo_pollution2019= tempSeoulGep.merge(Seoulmod2019, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)

maxdata=Seoulmodoverall.iloc[:,2:].max()
mindata=Seoulmodoverall.iloc[:,2:].min()



f, axes = plt.subplots(figsize=(8, 5), ncols=3, nrows=3,layout="compressed")
SeoulGeo_pollution2017.plot(ax=axes[0][0], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
SeoulGeo_pollution2017.plot(ax=axes[0][1], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
SeoulGeo_pollution2017.plot(ax=axes[0][2], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
SeoulGeo_pollution2018.plot(ax=axes[1][0], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
SeoulGeo_pollution2018.plot(ax=axes[1][1], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
SeoulGeo_pollution2018.plot(ax=axes[1][2], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
SeoulGeo_pollution2019.plot(ax=axes[2][0], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
SeoulGeo_pollution2019.plot(ax=axes[2][1], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
SeoulGeo_pollution2019.plot(ax=axes[2][2], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
for i, ax_row in enumerate(axes):
    for j, ax in enumerate(ax_row):
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Set title for the first column in each row
        if j == 1:
            ax.set_title("2017" if i == 0 else "2019", fontsize=16)

st.pyplot(f)


# test = pd.DataFrame(pollution)
# st.dataframe(pollution)