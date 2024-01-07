
import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import seaborn as sns
import requests
import geopandas as gpd
import os
import zipfile
from pmdarima import auto_arima
import time 
from sklearn import preprocessing
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

st.markdown("# Data Collection/Cleaning/Exploratory")
st.markdown(''' Since pollution is the main problem nowadays, I can find very good sources of South Korea pollution data. So, I decided to select 2 dataset''')

zf1 = zipfile.ZipFile('./projects/pollution/Korea.zip') 
pollution = pd.read_csv(zf1.open('south-korean-pollution-data.csv'))
zf2 = zipfile.ZipFile('./projects/pollution/Seoul.zip') 
Seoul = pd.read_csv(zf2.open('Measurement_summary.csv'))

def removezero(data):
    temp = Seoul.iloc[:,5:]  
    Avg = temp.mean()
    temp[temp<0] = np.nan
    for i in range(6):
        temp.iloc[:,lambda temp : i].replace(np.nan, Avg[i], inplace=True)
        Seoul.iloc[:,5:] = temp.iloc[:,0:]  
    return Seoul

removezero(Seoul)

datareading = '''zf1 = zipfile.ZipFile('./projects/pollution/Korea.zip') 
pollution = pd.read_csv(zf1.open('south-korean-pollution-data.csv'))
zf2 = zipfile.ZipFile('./projects/pollution/Seoul.zip') 
Seoul = pd.read_csv(zf2.open('Measurement_summary.csv'))
'''
st.code(datareading, language='python')


st.markdown(''' We found that the data is collected very hours and also contain detailed address and measured pollution in specific unit\
     Moreover, there are some anomaly data point which give negative value, so I will replace it by average of the column. The first\
          10 row of data is given as follows''')

st.dataframe(Seoul.head(5))


st.markdown(''' To perform exploratory data analysis, one can see that detailed Address and measuring time are too exceed. What we can do first to explore the data\
     is reducing the problem by considering just district and average over a year of polutions (data provide just 3 years). ''')
# st.markdowm(''' We first normalize data for each column to simple ''')
# unlike in Jupiter .groupby('').mean() in streamlit is require one culumns. So, I decited to droup all important column

def SeoulModify():
    Seoulmod = Seoul.copy()
    Seoulmod["Measurement date"]=Seoulmod["Measurement date"].str.slice(0,4)
    Seoulmod["Address"]=Seoulmod["Address"].str.split(',').str[2].str.strip()
    Seoulmod = Seoulmod.drop(["Latitude","Longitude","Station code"],axis=1)

    Seoulmodoverall =Seoulmod.drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
    Seoulmod2017=Seoulmod[Seoulmod["Measurement date"]=="2017"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
    Seoulmod2018=Seoulmod[Seoulmod["Measurement date"]=="2018"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
    Seoulmod2019=Seoulmod[Seoulmod["Measurement date"]=="2019"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
    return Seoulmodoverall,Seoulmod2017,Seoulmod2018,Seoulmod2019

st.markdown('''**_Now we get more clean dataset in the absence of unnesscary data for now_**''')

with st.spinner("Cleaning Data"):
    Seoulmodoverall,Seoulmod2017,Seoulmod2018,Seoulmod2019 = SeoulModify()
    st.dataframe(Seoulmod2017.head(6))

st.info(''' What we done here is nothing but group the data by extract just district and then calculate the averge over a year of each type of pollution by grouping\
    such district.''')
# show_btn = st.button("Show code!")
# if click:
#     st.session_state.more_stuff = True
# if show_btn:
#     SeoulModifyccode = ''' Seoulmod = Seoul.copy()
#     Seoulmod["Measurement date"]=Seoulmod["Measurement date"].str.slice(0,4)
#     Seoulmod["Address"]=Seoulmod["Address"].str.split(',').str[2].str.strip()
#     Seoulmod = Seoulmod.drop(["Latitude","Longitude","Station code"],axis=1)

#     Seoulmodoverall =Seoulmod.drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
#     Seoulmod2017=Seoulmod[Seoulmod["Measurement date"]=="2017"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
#     Seoulmod2018=Seoulmod[Seoulmod["Measurement date"]=="2018"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
#     Seoulmod2019=Seoulmod[Seoulmod["Measurement date"]=="2019"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()'''
#     st.code(SeoulModifyccode,language = 'python')

st.markdown(''' We now can map the pollution data onto each district and see the overall change over the years. In this work, I will use non-interactive map\
    and the best package to do such thing is **_Geopandas_**, Since the geo.json file contain district, we can group data from our cleaned dataset into\
        geometric file by grouping "Address". As a result, we can visualize the data on the Seoul's district as follows''')
 
def Geomerge() :
    tempSeoulGep=gpd.read_file("./projects/pollution/seoul_municipalities_geo.json")
    SeoulGeo_pollution2017= tempSeoulGep.merge(Seoulmod2017, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)
    SeoulGeo_pollution2018= tempSeoulGep.merge(Seoulmod2018, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)
    SeoulGeo_pollution2019= tempSeoulGep.merge(Seoulmod2019, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)
    maxdata=Seoulmodoverall.iloc[:,1:].max()
    mindata=Seoulmodoverall.iloc[:,1:].min()
    return SeoulGeo_pollution2017,SeoulGeo_pollution2018,SeoulGeo_pollution2019,maxdata,mindata

with st.spinner("Embedding Pollution data on Seoul Map!"):
    SeoulGeo_pollution2017,SeoulGeo_pollution2018,SeoulGeo_pollution2019,maxdata,mindata = Geomerge()

def plotgeo() :
    f, axes = plt.subplots(figsize=(5, 15), ncols=3, nrows=4,layout="compressed")
    SeoulGeo_pollution2017.plot(ax=axes[0][0], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
    SeoulGeo_pollution2017.plot(ax=axes[1][0], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
    SeoulGeo_pollution2017.plot(ax=axes[2][0], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
    SeoulGeo_pollution2017.plot(ax=axes[3][0], column='SO2', cmap='OrRd', legend=True, legend_kwds={"label": "SO2", "orientation": "horizontal"},vmin = mindata["SO2"],vmax = maxdata["SO2"])
    SeoulGeo_pollution2018.plot(ax=axes[0][1], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
    SeoulGeo_pollution2018.plot(ax=axes[1][1], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
    SeoulGeo_pollution2018.plot(ax=axes[2][1], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
    SeoulGeo_pollution2018.plot(ax=axes[3][1], column='SO2', cmap='OrRd', legend=True, legend_kwds={"label": "SO2", "orientation": "horizontal"},vmin = mindata["SO2"],vmax = maxdata["SO2"])
    SeoulGeo_pollution2019.plot(ax=axes[0][2], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
    SeoulGeo_pollution2019.plot(ax=axes[1][2], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
    SeoulGeo_pollution2019.plot(ax=axes[2][2], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
    SeoulGeo_pollution2019.plot(ax=axes[3][2], column='SO2', cmap='OrRd', legend=True, legend_kwds={"label": "SO2", "orientation": "horizontal"},vmin = mindata["SO2"],vmax = maxdata["SO2"])

    for i, ax_row in enumerate(axes):
        for j, ax in enumerate(ax_row):
            ax.set_xticks([])
            ax.set_yticks([])
            if i ==0:
                if j == 0:
                    ax.set_title("2017" , fontsize=12)
                elif j==1:
                    ax.set_title("2018" , fontsize=12)
                else:
                    ax.set_title("2019" , fontsize=12)
            else:
                ax.set_title(" ")
    return f, axes

st.subheader("EDA 1: Averaged Pollution of each year on different districts")
with st.spinner("The Mapping plot is generating, please wait"):
    f, axes = plotgeo()
    st.pyplot(f)

# show_btn = st.button("Show code! (This might take few seconds)")
# if click:
#     st.session_state.more_stuff = True
# if show_btn:
#     geocode = ''' tempSeoulGep=gpd.read_file("./projects/pollution/seoul_municipalities_geo.json")
# SeoulGeo_pollution2017= tempSeoulGep.merge(Seoulmod2017, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)
# SeoulGeo_pollution2018= tempSeoulGep.merge(Seoulmod2018, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)
# SeoulGeo_pollution2019= tempSeoulGep.merge(Seoulmod2019, left_on='SIG_ENG_NM', right_on='Address').drop("Address",axis=1)
# Seoulmod = Seoul.copy()
# Seoulmod["Measurement date"]=Seoulmod["Measurement date"].str.slice(0,4)
# Seoulmod["Address"]=Seoulmod["Address"].str.split(',').str[2].str.strip()
# Seoulmod = Seoulmod.drop(["Latitude","Longitude","Station code"],axis=1)

# Seoulmodoverall =Seoulmod.drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
# Seoulmod2017=Seoulmod[Seoulmod["Measurement date"]=="2017"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
# Seoulmod2018=Seoulmod[Seoulmod["Measurement date"]=="2018"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index()
# Seoulmod2019=Seoulmod[Seoulmod["Measurement date"]=="2019"].drop(["Measurement date"],axis=1).groupby('Address').mean().reset_index() 

# f, axes = plt.subplots(figsize=(5, 15), ncols=3, nrows=4,layout="compressed")
#     SeoulGeo_pollution2017.plot(ax=axes[0][0], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
#     SeoulGeo_pollution2017.plot(ax=axes[1][0], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
#     SeoulGeo_pollution2017.plot(ax=axes[2][0], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
#     SeoulGeo_pollution2017.plot(ax=axes[3][0], column='SO2', cmap='OrRd', legend=True, legend_kwds={"label": "SO2", "orientation": "horizontal"},vmin = mindata["SO2"],vmax = maxdata["SO2"])
#     SeoulGeo_pollution2018.plot(ax=axes[0][1], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
#     SeoulGeo_pollution2018.plot(ax=axes[1][1], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
#     SeoulGeo_pollution2018.plot(ax=axes[2][1], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
#     SeoulGeo_pollution2018.plot(ax=axes[3][1], column='SO2', cmap='OrRd', legend=True, legend_kwds={"label": "SO2", "orientation": "horizontal"},vmin = mindata["SO2"],vmax = maxdata["SO2"])
#     SeoulGeo_pollution2019.plot(ax=axes[0][2], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
#     SeoulGeo_pollution2019.plot(ax=axes[1][2], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
#     SeoulGeo_pollution2019.plot(ax=axes[2][2], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
#     SeoulGeo_pollution2019.plot(ax=axes[3][2], column='SO2', cmap='OrRd', legend=True, legend_kwds={"label": "SO2", "orientation": "horizontal"},vmin = mindata["SO2"],vmax = maxdata["SO2"])

#     for i, ax_row in enumerate(axes):
#         for j, ax in enumerate(ax_row):
#             ax.set_xticks([])
#             ax.set_yticks([])
#             if i ==0:
#                 if j == 0:
#                     ax.set_title("2017" , fontsize=12)
#                 elif j==1:
#                     ax.set_title("2018" , fontsize=12)
#                 else:
#                     ax.set_title("2019" , fontsize=12)
#             else:
#                 ax.set_title(" ")

# st.pyplot(f)'''
#     st.code(geocode,language = 'python')
# test = pd.DataFrame(pollution)
# st.dataframe(pollution)

st.info(''' From above data analysis, one can see that **_PM2.5_** is significantly increase during this 3 years. However, it is not really clear, how\
    it change in time. Therefore is it a good idea to investigate how it change over months.''')


Seoulmod1 = Seoul.copy()
Seoulmod1["Measurement date"]=Seoulmod1["Measurement date"].str.slice(0,7)
Seoulmod1["Address"]=Seoulmod1["Address"].str.split(',').str[2].str.strip()
Seoulmod1=Seoulmod1.drop(["Station code","Address","Latitude","Longitude"],axis=1).groupby(["Measurement date"]).mean().reset_index()

def plot_air_quality(Seoulmod1):
    # Convert the "Measurement date" column to datetime
    f, axes = plt.subplots(figsize=(15, 5), ncols=3, nrows=2, sharex=True)

    Seoulmod1.plot(ax=axes[0][0], y="PM2.5", x="Measurement date")
    Seoulmod1.plot(ax=axes[0][1], y="PM10", x="Measurement date")
    Seoulmod1.plot(ax=axes[0][2], y="CO", x="Measurement date")
    Seoulmod1.plot(ax=axes[1][0], y="SO2", x="Measurement date")
    Seoulmod1.plot(ax=axes[1][1], y="NO2", x="Measurement date")
    Seoulmod1.plot(ax=axes[1][2], y="O3", x="Measurement date")

    for ax in axes.flat:
        # Rotate x-axis labels
        ax.tick_params(axis='x', rotation=45)

    axes[0][0].set_xlabel("Year-Month")
    axes[0][0].set_ylabel("PM 2.5")
    axes[0][1].set_xlabel("Year-Month")
    axes[0][1].set_ylabel("PM10")
    axes[0][2].set_xlabel("Year-Month")
    axes[0][2].set_ylabel("CO")
    axes[1][0].set_xlabel("Year-Month")
    axes[1][0].set_ylabel("SO2")
    axes[1][1].set_xlabel("Year-Month")
    axes[1][1].set_ylabel("NO2")
    axes[1][2].set_xlabel("Year-Month")
    axes[1][2].set_ylabel("O3")

    plt.tight_layout()
    return f, axes

# Assuming Seoulmod1 is your DataFrame
# Call the function to plot the air quality parameters

st.subheader('EDA 2: Time Series Analysis')
with st.spinner("The Mapping plot is generating, please wait"):
    f, axes = plot_air_quality(Seoulmod1)
    st.pyplot(f)

st.markdown(''' What we found here is that, the air quality of Seoul, korea have periodicity. As a physicist, I will brifly evaluate the period of the\
     periodicity by using **_trigonometric function_** ''')

def cosfit():
    f, axes = plt.subplots(figsize=(15, 5), ncols=3, nrows=1, sharex=True)
    xcos= np.arange(len(Seoulmod1["Measurement date"]))
    fcos1 = 30+np.cos(12*xcos+1.5)*10
    fcos2 = 50+np.cos(12*xcos+1.5)*15
    fcos3 = 0.6+np.cos(12*xcos+0.5)*0.2

    Seoulmod1.plot(ax=axes[0], y="PM2.5", x="Measurement date")
    axes[0].plot(xcos,fcos1)
    Seoulmod1.plot(ax=axes[1], y="PM10", x="Measurement date")
    axes[1].plot(xcos,fcos2)
    Seoulmod1.plot(ax=axes[2], y="CO", x="Measurement date")
    axes[2].plot(xcos,fcos3)

    for ax in axes.flat:
            # Rotate x-axis labels
            ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()

    return f,axes
f,axes = cosfit()

st.pyplot(f)
st.info(''' We can see that the period of the data is approximatly 12 months, since we use the following cosine functions. Not just only PM2.5 but also\
    other pollution types.''')
st.latex(r''' \text{fit} = \text{shifting constant}+\cos(12 t  + \text{arbitrary phase })\\
    \text{So, we will use this period in model construction.}''')

st.markdown("# Model Selection/Training/Evaluation")
st.markdown(''' Since we found the periodic osillating data, we select the time-series ML tools to predict the data. We first a little bit more clean\
    the data by normalize it. This becuase we can compare our data with other dataset easily since they were collected in differnt unit and station''')

def scaling(data):
    scaled = preprocessing.MinMaxScaler().fit_transform(data)
    return scaled

st.dataframe(scaling(Seoulmod1.iloc[:,1::]))

