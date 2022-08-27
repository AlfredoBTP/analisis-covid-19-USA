#Librerias a utilizar
from ast import increment_lineno
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as pg


df_completo= pd.read_csv('df.csv')
df_completo = df_completo.drop_duplicates()
#Titulo para nuestro Dashboard
st.title("Hospitalización y muertes por estado (E.U.A)")
poblacion = pd.DataFrame({'Estados': ['California', 'Texas', 'Florida', 'Nueva York', 'Pennsylvania'], 'Población': ['39.5millones', '28.7millones', '21.2millones', '19.5millones','12.8millones']})
st.markdown('## Estados con mayor poblacion en E.U.A.')
st.table(poblacion)
#Filtre por fecha, sustitui valores faltantes por 0 e hice cast a las columnas para sumalas
df_completo.rename(columns={'state':'Estado','total_pediatric_patients_hospitalized_confirmed_covid':'Total_confirmados_pediatricos','total_adult_patients_hospitalized_confirmed_covid':'Total_confirmados_adultos'}, inplace=True)
df_completo['Total_confirmados_pediatricos'].fillna(0)
df_completo['Total_confirmados_pediatricos'].astype(float)
df_completo['Total_confirmados_adultos'].fillna(0)
df_completo['Total_confirmados_adultos'].astype(float)
df_completo.rename(columns={'staffed_icu_adult_patients_confirmed_covid':'Total_confirmados_adultos_ICU','staffed_icu_pediatric_patients_confirmed_covid':'Total_confirmados_pediatricos_ICU'}, inplace=True)
df_completo['Total_confirmados_pediatricos_ICU'].fillna(0)
df_completo['Total_confirmados_pediatricos_ICU'].astype(float)
df_completo['Total_confirmados_adultos_ICU'].fillna(0)
df_completo['Total_confirmados_adultos_ICU'].astype(float)
df_completo['Total_confirmados_UCI'] = df_completo['Total_confirmados_pediatricos_ICU']+ df_completo['Total_confirmados_adultos_ICU']
df_completo['Total de hospitalizados'] = df_completo['Total_confirmados_pediatricos'
            ]+ df_completo['Total_confirmados_adultos']

enfermos_tot =df_completo.groupby(['Estado'])[['Total de hospitalizados']].sum()
#Muertes nivel nacional
df_completo.rename(columns={'deaths_covid':'Muertes por covid'},inplace=True)
df_completo['Muertes por covid'].fillna(0)
df_completo['Muertes por covid'].astype(float)
muertes_tot =df_completo.groupby(['Estado'])[['Muertes por covid']].sum()
muertes_tot['Muertes por covid'] = round((muertes_tot['Muertes por covid']),0)

fig1 = px.bar(muertes_tot,x=  muertes_tot.index, y = muertes_tot['Muertes por covid'])
 
fig2 = px.bar(enfermos_tot, x= enfermos_tot.index, y = enfermos_tot['Total de hospitalizados'])
st.markdown('## Hospitalizados de covid por estado')
st.plotly_chart(fig2)
data = dict(type = 'choropleth', 
 locations = enfermos_tot.index, 
 locationmode = 'USA-states', 
 z = enfermos_tot['Total de hospitalizados'], 
 )
layout = dict(geo = {'scope':'usa'})
fig11 = pg.Figure(data = [data] ,
layout = layout)
st.markdown('## Mapa de hospitalizados')
st.plotly_chart(fig11)

st.markdown('## Muertes por covid en cada estado')
st.plotly_chart(fig1)
data = dict(type = 'choropleth', 
 locations = muertes_tot.index, 
 locationmode = 'USA-states', 
 z = muertes_tot['Muertes por covid'], 
 )
layout = dict(geo = {'scope':'usa'})
fig11 = pg.Figure(data = [data] ,
layout = layout)
st.markdown('## Mapa muertes por covid')
st.plotly_chart(fig11)
