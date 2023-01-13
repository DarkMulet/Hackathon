# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 17:19:25 2023

@author: robin
"""
import base64
import streamlit as st
import json
import pickle
import sklearn
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import streamlit.components.v1 as components
import os
path=os.getcwd()


def attributeCoeff(postal, year):
    return coeff.loc[postal, year]["Scaled"]


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


def Write(string):
    st.markdown('<center><p class="big-font">'+string+'</p></center>', unsafe_allow_html=True)


def GetType(Type):
    if Type == "Appartment":
        return 0
    if Type == "House":
        return 1


with open("Coeff.pickle", "rb") as input_file:
    coeff = pickle.load(input_file)

with open("scaler.pickle", "rb") as input_file:
    scaler = pickle.load(input_file)

with open("postaux.pickle", "rb") as input_file:
    postaux = pickle.load(input_file)

dfML = pd.read_csv("DataFrame.csv")


def ML():

    st.markdown("""<style>.big-font {font-size:50px !important;}</style>""", unsafe_allow_html=True)
    
    scaler = MinMaxScaler()
    scaler.fit(dfML.drop(["prix/m2"], axis=1))
    X = scaler.transform(dfML.drop(["prix/m2"], axis=1))
    y = dfML["prix/m2"]
    model = LinearRegression()
    model.fit(X, y)
    
    
    Years=[2018,2019,2020,2021,2022,2023,2024]
    
    set_background(fr'{path}/ParisImage.jpg')
    
    Type = st.select_slider("Type of Housing :", ["Appartment", "House"])
    
    year= int(st.selectbox("Year :", Years))
    
    codePostal = int(st.selectbox('Postal Code :', postaux))
    
    Co=attributeCoeff(codePostal,year)
    
    Write(f"Coeff of cost = {round(Co, 2)}")
    
    m2 = int(st.text_input("Square Meters :", 100))
    pieces = int(st.text_input("Number of Rooms :", 4))
    
    values = [[abs(1-GetType(Type)), GetType(Type), pieces, m2, Co]]
    toPredict = scaler.transform(pd.DataFrame(values))
    
    prixm2 = int(model.predict(toPredict)[0])
    prix = int(m2*prixm2)
    
    Write(f"Price per m² : {prixm2} €/m2")
    Write(f"Price total : {prix} €")


def DV():

    # Use the full page instead of a narrow central column
    # Space out the maps so the first one is 2x the size of the other three
    c1, c2, c3, c4, c5, c6, c7, c8 = st.columns((1, 1, 1, 1,  1, 1, 1, 1))
    html_temp = "<div class='tableauPlaceholder' id='viz1673599584494' style='position: relative'><noscript><a href='#'><img alt='Real Eastate Dashboard ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Re&#47;RealEstateDashboard_16735995671000&#47;RealEastateDashboard&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='RealEstateDashboard_16735995671000&#47;RealEastateDashboard' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Re&#47;RealEstateDashboard_16735995671000&#47;RealEastateDashboard&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='fr-FR' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1673599584494');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1280px';vizElement.style.height='827px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1280px';vizElement.style.height='827px';} else { vizElement.style.width='100%';vizElement.style.height='1177px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"
    with c1:
        components.html(html_temp, width=1280, height=800)


page_names_to_funcs = {
    "Real Estate Analysis    👁️  ": DV,
    "Price Prediction    $": ML,
}

selected_page = st.sidebar.selectbox("Select Tool", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()


# streamlit run streamlit_app.py
