
import streamlit as st
import pandas as pd


@st.cache_data
def cargar_datos():
    return pd.read_csv("datos/fmcg_2022_2024.csv")
