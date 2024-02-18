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


zf1 = zipfile.ZipFile('./projects/SQL/Sales Data.zip') 
Sales = pd.read_csv(zf1.open('Sales Data.csv'))

st.dataframe(Sales.head(5))



