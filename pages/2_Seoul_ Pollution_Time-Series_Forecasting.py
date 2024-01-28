
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



st.markdown("# Seoul Air Quality/ Time-series Forecasting")
st.markdown('''I start doing this small project to summarize and apply the knowledge of myself study in data science and machine learning. Eventhough most of\
    Data analysis and Data science focusing on basic of scikit-learn but in this data set I found that scikit-learn cannot predict well. The problem is because\
    I found that the pollution data is **_Periodic_**, which will be show soon, so that we need a time-series ML model to predict them. This problem tickle me\
    to gain some knowledge by doing this project since I have never use time-series ML before.''')

st.markdown("# Define Problem")
st.markdown(''' As a foreigner who living in Korea for 3.5 years, I realize that every springs and some season, Seoul encouter with terrible pollution problem.\
    I would like to see the overall increasing and behavior of pollution in Seoul and find out what are the main causes of this problem (if it possible) .\
    In quantitative research sense, we will see how pollution in Seoul change over years and will find the correlation to other factor, weather, people's activities\
    and so-on. To answer the question **_How pollution in Seoul behave quantitatively and what are the causes?_**''')

st.markdown("# Data Collection/Cleansing/Exploratory")
st.markdown(''' Since pollution is the main problem nowadays, I can find very good sources of South Korea pollution data. So, I decided to select 2 dataset''')

zf1 = zipfile.ZipFile('./projects/pollution/Korea.zip') 
pollution = pd.read_csv(zf1.open('south-korean-pollution-data.csv'))
zf2 = zipfile.ZipFile('./projects/pollution/Seoul.zip') 
Seoul = pd.read_csv(zf2.open('Measurement_summary.csv'))

def removemissing(data):
    temp = Seoul.iloc[:,5:]  
    Avg = temp.mean()
    temp[temp<0] = np.nan
    for i in range(6):
        temp.iloc[:,lambda temp : i].replace(np.nan, Avg[i], inplace=True)
        Seoul.iloc[:,5:] = temp.iloc[:,0:]  
    return Seoul

removemissing(Seoul)

datareading = '''zf1 = zipfile.ZipFile('./projects/pollution/Korea.zip') 
pollution = pd.read_csv(zf1.open('south-korean-pollution-data.csv'))
zf2 = zipfile.ZipFile('./projects/pollution/Seoul.zip') 
Seoul = pd.read_csv(zf2.open('Measurement_summary.csv'))
'''
st.code(datareading, language='python')


st.markdown(''' We found that the data is collected very hours and also contain detailed address and measured pollution in specific unit\
     Moreover, there are some anomaly data point which give negative value, so I will replace it by average of the column. The first\
          10 rows of data is given as follows''')

st.dataframe(Seoul.head(5))


st.markdown(''' To perform exploratory data analysis, one can see that detailed address and measuring time are too exceed. What we can do to explore the data\
     is reducing the problem by considering just district and average over a year of polutions (data provide just 3 years). Moreover, we found the noise data\
         where the measured data is **_negativa values_**. We decide to replace these data by the average value of the type of pollutions ''')
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

st.markdown('''**_Now we get more clean dataset which is clean and there is no negative values or missing data_**''')

with st.spinner("Cleaning Data"):
    Seoulmodoverall,Seoulmod2017,Seoulmod2018,Seoulmod2019 = SeoulModify()
    st.dataframe(Seoulmod2017.head(6))

st.info(''' What we done here is nothing but group the data by extracting just district and then calculate the averge over a year of each type of pollution by grouping\
    such district.''')
 
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
    SeoulGeo_pollution2017.plot(ax=axes[0][0], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
    SeoulGeo_pollution2017.plot(ax=axes[1][0], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
    SeoulGeo_pollution2017.plot(ax=axes[2][0], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
    SeoulGeo_pollution2017.plot(ax=axes[3][0], column='SO2', cmap='OrRd', legend=True, legend_kwds={"label": "", "orientation": "horizontal"},vmin = mindata["SO2"],vmax = maxdata["SO2"])
    SeoulGeo_pollution2018.plot(ax=axes[0][1], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "PM2.5", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
    SeoulGeo_pollution2018.plot(ax=axes[1][1], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "PM10", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
    SeoulGeo_pollution2018.plot(ax=axes[2][1], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "CO", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
    SeoulGeo_pollution2018.plot(ax=axes[3][1], column='SO2', cmap='OrRd', legend=True, legend_kwds={"label": "SO2", "orientation": "horizontal"},vmin = mindata["SO2"],vmax = maxdata["SO2"])
    SeoulGeo_pollution2019.plot(ax=axes[0][2], column='PM2.5', cmap='OrRd', legend=True, legend_kwds={"label": "", "orientation": "horizontal"},vmin = mindata["PM2.5"],vmax = maxdata["PM2.5"])
    SeoulGeo_pollution2019.plot(ax=axes[1][2], column='PM10', cmap='OrRd', legend=True, legend_kwds={"label": "", "orientation": "horizontal"},vmin = mindata["PM10"],vmax = maxdata["PM10"])
    SeoulGeo_pollution2019.plot(ax=axes[2][2], column='CO', cmap='OrRd', legend=True, legend_kwds={"label": "", "orientation": "horizontal"},vmin = mindata["CO"],vmax = maxdata["CO"])
    SeoulGeo_pollution2019.plot(ax=axes[3][2], column='SO2', cmap='OrRd', legend=True, legend_kwds={"label": "", "orientation": "horizontal"},vmin = mindata["SO2"],vmax = maxdata["SO2"])

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

st.subheader("EDA 1: South Korea Air Quality by Different Districts")

st.markdown(''' We now can map the pollution data onto each district and see the overall change over the years. In this work, I will use non-interactive map\
    and the best package to do such thing is **_Geopandas_**, Since the geo.json file contain district, we can group data from our cleaned dataset into\
        geometric file by grouping "Address". As a result, we can visualize the data on the Seoul's district as follows''')

with st.spinner("The Mapping plot is generating, please wait"):
    f, axes = plotgeo()
    st.pyplot(f)

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

st.markdown('''**_We separate PM2.5 for each district. We will use bubble plot, each district contains 12 points data which are nothing other than data \
    for each month. Then we also sort the best to worst air quanlity district._**''')



with st.spinner("The plot is generating, please wait"):
    Seoulmod = Seoul.copy()
    Seoulmod["Measurement date"]=Seoulmod["Measurement date"].str.slice(0,7)
    Seoulmod["Address"]=Seoulmod["Address"].str.split(',').str[2].str.strip()
    Seoulmod = Seoulmod.drop(["Latitude","Longitude","Station code"],axis=1)
    Seoulmod.insert(0,"M",Seoulmod["Measurement date"].str.slice(5,7),True)
    Seoulmod.insert(1,"Y",Seoulmod["Measurement date"].str.slice(0,4),True)
    Seoulmod.drop("Measurement date",axis=1,inplace=True)
    A=Seoulmod.drop(["Y"],axis=1).groupby(["Address","M"],as_index = False).mean()
    fig = plt.figure(figsize=(12,5))
    meandata = A.sort_values(by="PM2.5").drop("M",axis=1).groupby("Address",as_index = False).mean()
    sns.scatterplot(data=A.sort_values(by="PM2.5"), x = "Address" , y= "PM2.5", hue="PM2.5", palette="icefire", size = "PM2.5")
    sns.lineplot(data= meandata, x = "Address" , y= "PM2.5", linestyle='--')
    plt.xticks(rotation=45, fontsize=9)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    st.pyplot(fig)

st.info(''' The result shows that the average best and worst air quality district is Jungnang-gu (중랑구) and Yeongdeungpo-gu (영등포구), respectively.''')

st.subheader('EDA 2: Correlations/ Regressions')
st.markdown(''' From the data, we can extract the correlations between data. One can see the strong possitive correlation between PM2.5 and PM10, CO and NO2. On the other hand, we found\
      kind of strong negative correlation between CO and O-zone (O3). ''')
with st.spinner("The plot is generating, please wait"):
    Btemp= A.drop(["Address","M"],axis=1)
    fig1 = plt.figure(figsize=(12,5))
    corr= Btemp.corr()
    matrix = np.triu(corr)
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr,annot=True, mask=matrix, cmap=cmap)
    st.pyplot(fig1)

st.markdown(''' We then shows some examples of correlations between each pollution which appear as possitive, negative, and no correlation as follows respectively. ''')

with st.spinner("The plot is generating, please wait"):
    fig,axes = plt.subplots(figsize=(6, 6), ncols=2, nrows=3,layout="compressed")
    sns.regplot(x="PM2.5",y="PM10",data = Btemp, ax=axes[0,0],line_kws={"color": "red"})
    sns.residplot(x="PM2.5",y="PM10",data = Btemp, ax=axes[0,1])
    sns.regplot(x="O3",y="CO",data = Btemp, ax=axes[1,0],line_kws={"color": "red"})
    sns.residplot(x="O3",y="CO",data = Btemp, ax=axes[1,1])
    sns.regplot(x="O3",y="SO2",data = Btemp, ax=axes[2,0],line_kws={"color": "red"})
    sns.residplot(x="O3",y="SO2",data = Btemp, ax=axes[2,1])
    st.pyplot(fig)


st.subheader('EDA 3: Time Series Analysis/ Forcasting')
Seoulmod = Seoul.copy()
Seoulmod["Measurement date"]=Seoulmod["Measurement date"].str.slice(0,7)
Seoulmod["Address"]=Seoulmod["Address"].str.split(',').str[2].str.strip()
Seoulmod = Seoulmod.drop(["Latitude","Longitude","Station code"],axis=1)
A = Seoulmod.groupby(["Measurement date","Address"],as_index= False).mean().drop("Address",axis=1)
A["Measurement date"] = A["Measurement date"].str.slice(0,7)
A.insert(7,"M",A["Measurement date"].str.slice(5,7),True)
A.insert(8,"Y",A["Measurement date"].str.slice(0,4),True)
A.drop("Measurement date",axis=1,inplace=True)
A=A.groupby(["M","Y"],as_index=False).mean()


with st.spinner("The plot is generating, please wait"):
    fig = plt.figure(figsize=(8,5))
    sns.scatterplot(data=A, x='M', y='PM2.5', hue='Y', palette="icefire" ,size = "PM2.5")
    plt.xlabel('Month')
    plt.ylabel('PM 2.5')
    plt.title('Seasonality of Air Quality')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    st.pyplot(fig)


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

pollutionmod=pollution[pollution["District"]=="Seoul"].drop("Unnamed: 0",axis=1)[::-1].reset_index().drop("index",axis=1)
pollutionmod["date"]=pollutionmod["date"].str.replace("/", "-")
temp=pollutionmod.copy()
i=0
while i < (pollutionmod.shape)[0]:
    n = temp['date'][i].rfind("-")
    pollutionmod.loc[i,'date'] = (temp['date'][i][0:n])
    i=i+1
i=0
while i < (pollutionmod.shape)[0]:
    if len(pollutionmod['date'][i]) <= 6:
        pollutionmod.loc[i,'date']=pollutionmod.loc[i,'date'].replace("-","-0")
        i=i+1
    else:
        i=i+1

Cleanpollution=pollutionmod.drop(["District","Country","Lat","Long"],axis=1)
Cleanpollution=Cleanpollution.groupby(["City","date"]).mean().reset_index()
Cleanpollution=Cleanpollution[Cleanpollution["City"]=="Nowon-Gu"].sort_values(by="date").reset_index(drop=True)
Cleanpollution = Cleanpollution.reset_index()
Cleanpollution=Cleanpollution.drop(["City","index"],axis=1).groupby(["date"]).mean().reset_index()

def MLfor(Seoulmod1):
    train_x=(Seoulmod1.reset_index())[["index"]]
    train_y1= Seoulmod1["PM2.5"]
    x_test = pd.DataFrame(np.arange(35,62))
    x_test.index = np.arange(35,62)
    modelpm25 = auto_arima(y = train_y1,X = train_x , m = 12)
    prediction25= modelpm25.predict(n_periods= 27,X=x_test)
    prediction25.index = Cleanpollution.iloc[71:98,0]
    return prediction25

def plotfor(predict):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    # Plotting with labels
    line1, = ax1.plot(Seoulmod1["Measurement date"], Seoulmod1["PM2.5"], label='Dataset')
    line2, = ax1.plot(predict, label='Machine Learning  Prediction')

    # Specify the legends
    legend1 = ax1.legend(handles=[line1], loc='upper left')
    legend2 = ax1.legend(handles=[line2], loc='lower right')

    # Add the legends to the plot
    ax1.add_artist(legend1)
    ax1.add_artist(legend2)

    N = 7
    ax1.set_xticks(Cleanpollution["date"][37::N])
    ax1.set_xticklabels(Cleanpollution["date"][37::N], rotation=45, fontsize=9)
    return fig

plt.show()

st.markdown('''The first ML module I will use is <span style="color:blue">some *blue* text</span>.
, which is the module for time-series forecasting. We first consider year-time scale. The result is given as follows''')
with st.spinner("Training Model"):
    prediction25 = MLfor(Seoulmod1)
    fig = plotfor(prediction25)
    st.pyplot(fig)

st.markdown('''The first ML module I will use is auto_arima, which is a module for time-series forecasting. We first consider year-time scale. The result is given as follows''')

Seoulmod = Seoul.copy()
Seoulmod["Measurement date"]=Seoulmod["Measurement date"].str.slice(0,10)
Seoulmod["Address"]=Seoulmod["Address"].str.split(',').str[2].str.strip()
Seoulmod=Seoulmod.drop(["Station code","Address","Latitude","Longitude"],axis=1).groupby(["Measurement date"]).mean().reset_index()


def MLfor(Seoulmod1):
    train_x=(Seoulmod1.reset_index())[["index"]]
    train_y1= Seoulmod1["PM2.5"]
    x_test = pd.DataFrame(np.arange(35,62))
    x_test.index = np.arange(35,62)
    modelpm25 = auto_arima(y = train_y1,X = train_x , m = 12)
    prediction25= modelpm25.predict(n_periods= 27,X=x_test)
    prediction25.index = Cleanpollution.iloc[71:98,0]
    return prediction25

st.markdown("Since the day-scaled data forcasting take to long time to train the model. So, I will not add the complied code in this app ")