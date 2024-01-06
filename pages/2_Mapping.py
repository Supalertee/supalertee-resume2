
import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import geopandas as gpd
import os
from pmdarima import auto_arima

from sklearn.metrics import r2_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import confusion_matrix, accuracy_score
import sklearn.metrics as metrics

pollution = pd.read_csv("./projects/pollution/south-korean-pollution-data.csv")

test = pd.DataFrame(pollution)
st.dataframe(pollution)