# dashboard_obj2.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración general
st.set_page_config(layout="wide")
st.title("Dashboard - Objetivo 2: Zonas de Riesgo de Femicidios en Ecuador")

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_excel("../datos_wendy.xlsx")

df = cargar_datos()

# ======= FIGURA 5: Distribución por tipo de muerte =======
st.markdown("### Distribución por Tipo de Muerte")

col1, col2 = st.columns([2, 1])  # ancho 2:1 para imagen:texto

with col1:
    # Gráfico de barras: tipo de muerte
    conteo_tipo = df['Tipomuerte_SRMCE2'].value_counts()
    colores = ['blue' if tipo == 'OTRAS MUERTES VIOLENTAS' else 'orange' for tipo in conteo_tipo.index]

    fig1, ax1 = plt.subplots(figsize=(6,4))
    ax1.bar(conteo_tipo.index, conteo_tipo.values, color=colores)
    ax1.set_xlabel('Tipo de Muerte')
    ax1.set_ylabel('Cantidad de Casos')
    st.pyplot(fig1)

with col2:
    st.markdown("""
    **La Figura** muestra la distribución de casos según el tipo de muerte,  
    permitiendo visualizar la cantidad de femicidios en comparación  
    con otras muertes violentas.
    """)

# ======= FIGURA 6: Distribución por provincia =======
st.markdown("### Distribución Geográfica por Provincia")

col3, col4 = st.columns([2, 1])

with col3:
    # Gráfico de barras horizontal: porcentaje por provincia
    provincia_counts = df['Provincia'].value_counts(normalize=True).sort_values(ascending=False) * 100

    fig2, ax2 = plt.subplots(figsize=(12, 5))
    sns.barplot(x=provincia_counts.index, y=provincia_counts.values, palette="Spectral", ax=ax2)
    ax2.set_ylabel("Porcentaje (%)")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=60, ha="right")
    st.pyplot(fig2)

with col4:
    st.markdown("""
    Con el objetivo de analizar la distribución geográfica de los casos  
    de femicidios y muertes violentas de mujeres en Ecuador,  
    a continuación, se ilustra la distribución de casos por provincia.
    """)

import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.markdown("### Mapa de Calor con Marcadores")

col5, col6 = st.columns([2, 1])

with col5:
    if {'Latitud', 'Longitud', 'Provincia'}.issubset(df.columns):
        provincias_clave = ['GUAYAS', 'PICHINCHA', 'MANABÍ', 'LOS RÍOS', 'ESMERALDAS']
        df_filtrado = df[df['Provincia'].str.upper().isin(provincias_clave)].dropna(subset=['Latitud', 'Longitud'])

        mapa = folium.Map(location=[-1.8312, -78.1834], zoom_start=6)

        # Capa de calor
        heat_data = df_filtrado[['Latitud', 'Longitud']].values.tolist()
        HeatMap(
            heat_data,
            radius=14,
            blur=12,
            min_opacity=0.5,
            max_zoom=7
        ).add_to(mapa)

        
        st_folium(mapa, width=700, height=500)

    else:
        st.warning("No se encuentran las columnas 'lat', 'lon' y 'PROVINCIA' en los datos.")

with col6:
    st.markdown("""
    **Figura .** Visualización de los casos de violencia fatal  
    en Ecuador. El mapa combina un mapa de calor con círculos  
    que marcan cada incidente individual dentro de las provincias  
    más afectadas.
    """)

# ======= FIGURA 8: Distribución Temporal =======
import seaborn as sns
import matplotlib.pyplot as plt

st.markdown("### Distribución Temporal de Casos")

# Crear dos columnas para gráficos lado a lado
col1, col2 = st.columns(2)

with col1:
    # Orden de los meses en español
    meses_ordenados = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                       'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    df['Mes'] = pd.Categorical(df['Mes'].str.lower(), categories=meses_ordenados, ordered=True)
    conteo_mes = df['Mes'].value_counts().sort_index()
    conteo_mes = df['Mes'].str.lower().value_counts().sort_values(ascending=False)

    fig_mes, ax_mes = plt.subplots(figsize=(6,4))
    sns.barplot(x=conteo_mes.index, y=conteo_mes.values, palette='viridis', ax=ax_mes)
    ax_mes.set_xlabel("Mes")
    ax_mes.set_ylabel("Cantidad de Casos")
    ax_mes.tick_params(axis='x', rotation=45)
    st.pyplot(fig_mes)

with col2:
    dias_ordenados = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    df['Dia'] = pd.Categorical(df['Dia'].str.lower(), categories=dias_ordenados, ordered=True)
    conteo_dia = df['Dia'].str.lower().value_counts().sort_values(ascending=False)

    fig_dia, ax_dia = plt.subplots(figsize=(6,4))
    sns.barplot(x=conteo_dia.index, y=conteo_dia.values, palette='viridis', ax=ax_dia)
    ax_dia.set_xlabel("Día de la Semana")
    ax_dia.set_ylabel("Cantidad de Casos")
    ax_dia.tick_params(axis='x', rotation=45)
    st.pyplot(fig_dia)

# Texto explicativo
st.markdown("""
**Figura .** Para identificar patrones temporales,  
se procedió a realizar un análisis de la distribución de casos  
por **meses** y **días de la semana**.  
Esto permite comprender la variación de la violencia fatal en el tiempo.
""")


# ======= FIGURA 9: Análisis de Tendencias Temporales =======
import matplotlib.pyplot as plt

st.markdown("### Tendencia Mensual de Casos de Violencia Fatal")

# Orden correcto de los meses
meses_ordenados = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                   'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
df['Mes'] = pd.Categorical(df['Mes'].str.lower(), categories=meses_ordenados, ordered=True)
conteo_mes = df['Mes'].value_counts().sort_index()

# Gráfico de línea
fig_tendencia, ax = plt.subplots(figsize=(8, 5))
ax.plot(conteo_mes.index, conteo_mes.values, color='orange', marker='o', linewidth=2)
ax.set_xlabel("Mes")
ax.set_ylabel("Cantidad de Casos")
ax.set_title("Tendencia mensual de casos de violencia fatal")
ax.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig_tendencia)

# Descripción textual
st.markdown("""
**Figura.** *Análisis de Tendencias Temporales.*  
Se presenta la evolución de los casos de violencia fatal contra mujeres  
a lo largo de los meses del año. Este análisis permite identificar  
patrones estacionales y periodos con mayor incidencia.
""")


# ======= FIGURA 10: Distribución de Edad de las Víctimas =======
import seaborn as sns
import matplotlib.pyplot as plt

st.markdown("### Distribución de la Edad de las Víctimas ")

# Verificamos columnas necesarias
if {'Edad_Victima', 'Tipomuerte_SRMCE2'}.issubset(df.columns):
    # Filtrar por tipos válidos y eliminar nulos
    df_edad = df[df['Edad_Victima'].notna() & df['Tipomuerte_SRMCE2'].notna()]
    df_edad = df_edad[df_edad['Edad_Victima'] <= 100]  # limitar valores extremos

    fig_edades, ax = plt.subplots(figsize=(10, 5))

    # Histograma con KDE para cada tipo de muerte
    sns.histplot(data=df_edad[df_edad['Tipomuerte_SRMCE2'] == 'FEMICIDIO'],
                 x='Edad_Victima', kde=True, color='red', label='Femicidios', stat='frequency', bins=30, alpha=0.5, ax=ax)
    
    sns.histplot(data=df_edad[df_edad['Tipomuerte_SRMCE2'] == 'OTRAS MUERTES VIOLENTAS'],
                 x='Edad_Victima', kde=True, color='blue', label='Otras muertes violentas', stat='frequency', bins=30, alpha=0.5, ax=ax)

    ax.set_title("Distribución de la Edad de las Víctimas")
    ax.set_xlabel("Edad")
    ax.set_ylabel("Frecuencia")
    ax.legend()
    st.pyplot(fig_edades)

    # Texto descriptivo
    st.markdown("""
    **Figura.** La distribución de la edad es ligeramente diferente  
    entre las víctimas de **femicidios** y de **otras muertes violentas**.  
    Las víctimas de femicidios tienden a ser un poco más jóvenes,  
    y la mayoría de los casos se concentran entre los **20 y 40 años**.
    """)
else:
    st.warning("⚠️ El dataset no contiene las columnas 'EDAD' y 'TIPO_MUERTE' necesarias para esta figura.")


# ======= FIGURA 11: Nivel de Educación de las Víctimas =======
import seaborn as sns
import matplotlib.pyplot as plt

st.markdown("### Distribución del Nivel de Educación de las Víctimas")

# Verificamos columnas necesarias
if {'NivelEducación_Victima', 'Tipomuerte_SRMCE2'}.issubset(df.columns):
    df_edu = df[df['NivelEducación_Victima'].notna() & df['Tipomuerte_SRMCE2'].notna()]

    # Orden personalizado (si aplica)
    orden_educacion = ['NINGUNO', 'INICIAL', 'EDUCACIÓN BÁSICA', 'BACHILLERATO', 'SUPERIOR']

    col1, col2 = st.columns(2)

    with col1:
        fem = df_edu[df_edu['Tipomuerte_SRMCE2'] == 'FEMICIDIO']
        conteo_fem = fem['NivelEducación_Victima'].value_counts().sort_values(ascending=False)
        fig_fem, ax1 = plt.subplots()
        sns.barplot(x=conteo_fem.index, y=conteo_fem.values, palette='Reds', alpha=0.7, ax=ax1)
        ax1.set_title("Nivel de Educación - Femicidios")
        ax1.set_xlabel("Nivel de Educación")
        ax1.set_ylabel("Frecuencia")
        ax1.tick_params(axis='x', rotation=45)
        st.pyplot(fig_fem)

    with col2:
        otras = df_edu[df_edu['Tipomuerte_SRMCE2'] == 'OTRAS MUERTES VIOLENTAS']
        conteo_otras = otras['NivelEducación_Victima'].value_counts().sort_values(ascending=False)
        fig_otras, ax2 = plt.subplots()
        sns.barplot(x=conteo_otras.index, y=conteo_otras.values, palette='Blues', alpha=0.7, ax=ax2)
        ax2.set_title("Nivel de Educación - Otras Muertes Violentas")
        ax2.set_xlabel("Nivel de Educación")
        ax2.set_ylabel("Frecuencia")
        ax2.tick_params(axis='x', rotation=45)
        st.pyplot(fig_otras)

    # Texto explicativo (opcional)
    st.markdown("""
    **Figura.** Distribución del nivel de educación de las víctimas  
    de femicidio y otras muertes violentas. Se observa una mayor concentración  
    en niveles de **educación básica y bachillerato**, con una proporción  
    significativamente baja en niveles de educación superior.
    """)
else:
    st.warning("⚠️ El dataset no contiene las columnas 'NIVEL_EDUCACION' y 'TIPO_MUERTE' necesarias para esta figura.")


# ======= FIGURA 12: Nivel de Educación de los Agresores =======
import seaborn as sns
import matplotlib.pyplot as plt

st.markdown("### Distribución del Nivel de Educación de los Agresores")

# Verificamos que exista la columna
if 'NivelEducación_Agresor' in df.columns:
    df_agresor = df[df['NivelEducación_Agresor'].notna()]

    # Conteo ordenado descendente
    conteo_agresor = df_agresor['NivelEducación_Agresor'].value_counts().sort_values(ascending=False)

    fig_agresor, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x=conteo_agresor.index, y=conteo_agresor.values, palette='viridis', ax=ax)
    ax.set_title("Distribución del Nivel de Educación de los Agresores")
    ax.set_xlabel("Nivel de Educación")
    ax.set_ylabel("Frecuencia")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig_agresor)

    # Texto opcional
    st.markdown("""
    **Figura.** Distribución del nivel educativo de los agresores.  
    La categoría **“No identificado”** representa la mayoría de los casos,  
    seguida por niveles de **educación básica** y **ninguno**, lo cual  
    podría estar vinculado a contextos de vulnerabilidad estructural.
    """)
else:
    st.warning("⚠️ No se encontró la columna 'NivelEducación_Agresor' en los datos.")


# ======= FIGURA 13: Distribución de la Edad de los Agresores =======
import seaborn as sns
import matplotlib.pyplot as plt

st.markdown("### Distribución de la Edad de los Agresores")

if 'Edad_Agresor' in df.columns:
    # Convertir a numérico y eliminar errores (como 'NO IDENTIFICADO')
    df['Edad_Agresor'] = pd.to_numeric(df['Edad_Agresor'], errors='coerce')
    df_edad_agresor = df[df['Edad_Agresor'].notna() & (df['Edad_Agresor'] <= 120)]

    fig_edad_agresor, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df_edad_agresor['Edad_Agresor'], bins=20, kde=True, color='orange', edgecolor='black', ax=ax)
    ax.set_xlabel("Edad del Agresor")
    ax.set_ylabel("Frecuencia")
    ax.set_title("Distribución de la Edad de los Agresores")
    st.pyplot(fig_edad_agresor)

    st.markdown("""
    **Figura .** La mayoría de los agresores se concentran  
    en el rango de **20 a 40 años**, con una disminución progresiva  
    a medida que la edad aumenta. Esta figura permite visualizar  
    la **tendencia general de edad** y la posible existencia de  
    **valores atípicos** en el conjunto de datos.
    """)
else:
    st.warning("⚠️ La columna 'Edad_Agresor' no está disponible en el dataset.")


# ======= FIGURA 14: Estado Civil de las Víctimas =======
import seaborn as sns
import matplotlib.pyplot as plt

st.markdown("### Distribución del Estado Civil de las Víctimas ")

if {'Estcivil_Victima', 'Tipomuerte_SRMCE2'}.issubset(df.columns):
    df_estado = df[df['Estcivil_Victima'].notna() & df['Tipomuerte_SRMCE2'].notna()]

    col1, col2 = st.columns(2)

    with col1:
        fem = df_estado[df_estado['Tipomuerte_SRMCE2'] == 'FEMICIDIO']
        conteo_fem = fem['Estcivil_Victima'].value_counts().sort_values(ascending=False)
        fig_fem, ax1 = plt.subplots()
        sns.barplot(x=conteo_fem.index, y=conteo_fem.values, palette='Reds', alpha=0.7, ax=ax1)
        ax1.set_title("Estado Civil - Femicidios")
        ax1.set_xlabel("Estado Civil")
        ax1.set_ylabel("Frecuencia")
        ax1.tick_params(axis='x', rotation=45)
        st.pyplot(fig_fem)

    with col2:
        otras = df_estado[df_estado['Tipomuerte_SRMCE2'] == 'OTRAS MUERTES VIOLENTAS']
        conteo_otras = otras['Estcivil_Victima'].value_counts().sort_values(ascending=False)
        fig_otras, ax2 = plt.subplots()
        sns.barplot(x=conteo_otras.index, y=conteo_otras.values, palette='Blues', alpha=0.7, ax=ax2)
        ax2.set_title("Estado Civil - Otras Muertes Violentas")
        ax2.set_xlabel("Estado Civil")
        ax2.set_ylabel("Frecuencia")
        ax2.tick_params(axis='x', rotation=45)
        st.pyplot(fig_otras)

    st.markdown("""
    **Figura.** Distribución del estado civil de las víctimas.  
    Se observa que la mayoría de las víctimas, tanto de femicidios como  
    de otras muertes violentas, se encontraban en condición de **soltería**,  
    seguidas por aquellas que eran **casadas** o **divorciadas**.  
    Este análisis permite identificar contextos relacionales potenciales  
    dentro de las situaciones de violencia letal.
    """)
else:
    st.warning("⚠️ El dataset no contiene las columnas 'ESTADO_CIVIL' y 'TIPO_MUERTE'.")


# ======= FIGURA 15: Edad de las Víctimas por Región =======
import seaborn as sns
import matplotlib.pyplot as plt

st.markdown("### Distribución de la Edad de las Víctimas por Región")

if {'Edad_Victima', 'Region'}.issubset(df.columns):
    df_region = df[df['Edad_Victima'].notna() & df['Region'].notna()]
    df_region = df_region[df_region['Edad_Victima'] <= 100]

    fig15, ax15 = plt.subplots(figsize=(10, 5))

    regiones = {'COSTA': 'red', 'SIERRA': 'blue', 'ORIENTE': 'green'}
    for region, color in regiones.items():
        data = df_region[df_region['Region'].str.upper() == region]
        sns.histplot(data['Edad_Victima'], kde=True, bins=30, label=region.capitalize(), color=color, ax=ax15, stat='frequency', alpha=0.5, edgecolor='black')

    ax15.set_title("Distribución de la Edad de las Víctimas por Región")
    ax15.set_xlabel("Edad")
    ax15.set_ylabel("Frecuencia")
    ax15.legend(title="Región")
    st.pyplot(fig15)

    st.markdown("""
    **Figura.** La distribución de la edad de las víctimas  
    en las regiones **Costa**, **Sierra** y **Oriente** muestra  
    diferentes patrones, donde la región Costa concentra la mayor  
    cantidad de casos en edades jóvenes.
    """)
else:
    st.warning("⚠️ Las columnas 'EDAD' y 'REGION' no están disponibles en el dataset.")

# ======= FIGURA 16: Edad de las Víctimas por Área =======
st.markdown("### Distribución de la Edad de las Víctimas por Área ")

if {'Edad_Victima', 'Area'}.issubset(df.columns):
    df_area = df[df['Edad_Victima'].notna() & df['Area'].notna()]
    df_area = df_area[df_area['Edad_Victima'] <= 100]

    fig16, ax16 = plt.subplots(figsize=(10, 5))

    areas = {'URBANA': 'blue', 'RURAL': 'green'}
    for area, color in areas.items():
        data = df_area[df_area['Area'].str.upper() == area]
        sns.histplot(data['Edad_Victima'], kde=True, bins=30, label=area.capitalize(), color=color, ax=ax16, stat='frequency', alpha=0.5, edgecolor='black')

    ax16.set_title("Distribución de la Edad de las Víctimas por Área")
    ax16.set_xlabel("Edad")
    ax16.set_ylabel("Frecuencia")
    ax16.legend(title="Área")
    st.pyplot(fig16)

    st.markdown("""
    **Figura.** Distribución de la edad de las víctimas en áreas  
    **urbanas** y **rurales**. Ambas áreas tienen un patrón de edad similar,  
    con un **pico alrededor de los 30 años**, aunque las zonas urbanas  
    muestran una mayor concentración de casos.
    """)
else:
    st.warning("⚠️ Las columnas 'EDAD' y 'AREA' no están disponibles en el dataset.")
