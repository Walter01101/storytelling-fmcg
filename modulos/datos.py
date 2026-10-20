
import streamlit as st
import pandas as pd

# True: español | False: inglés original
TRADUCIR = True


@st.cache_data
def cargar_datos():
    return pd.read_csv("datos/fmcg_2022_2024.csv")


def obtener_datos():
    df = cargar_datos().copy()

    if not TRADUCIR:
        return df

    # Traducir categorías
    df["category"] = df["category"].replace({
        "Yogurt": "Yogur",
        "Milk": "Leche",
        "ReadyMeal": "Comida preparada", # listos para consumir o precocidos
        "SnackBar": "Barra de cereal",
        "Juice": "Jugo"
    })

    # Traducir canales
    df["channel"] = df["channel"].replace({
        "Retail": "Tiendas minoristas",
        "E-commerce": "Comercio electrónico",
        "Discount": "Tiendas de descuento"
    })

    # Traducir segmentos
    df["segment"] = df["segment"].replace({
        "Premium": "Premium",
        "Regular": "Regular",
        "Budget": "Económico"
    })

    # Traducir tipos de empaque
    df["pack_type"] = df["pack_type"].replace({
        "Bottle": "Botella",
        "Box": "Caja",
        "Can": "Lata",
        "Bag": "Bolsa",
        "Pack": "Paquete"
    })

    return df
