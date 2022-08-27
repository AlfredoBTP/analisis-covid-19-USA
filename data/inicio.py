#Librerias a utilizar
import streamlit as st
import pandas as pd
import plotly.express as px
from sodapy import Socrata



st.title("Comportamiento de covid-19 durante la pandemia en E.U.A.")
df_completo= pd.read_csv("pages/df.csv")
client = Socrata("healthdata.gov", None)
results = client.get("g62h-syeh", limit=50000)
df_completo= pd.DataFrame.from_records(results)
df_completo = df_completo.drop_duplicates()
#Titulo para nuestro Dashboard

fechas = pd.DataFrame({'Fecha': ['14 de febrero del 2020', 'Marzo del 2020', 'Junio-Julio 2020', '14 de Diciembre 2020',
                     'Diciembre del 2020 y 2021', 'Julio del 2021'], 'Acontecimiento': ['Se detecta el primer caso de coivd-19 en U.S.A.', 
                     'Se declara cuarentena en la mayor parte del país', 'Se comienza a levantar la cuarentena', 
                     'Comienza la vacunación', 'Fiestas decembrinas', 'Regresan los eventos masivos']})
st.markdown('## Fechas y acontecimientos')
st.table(fechas)

df_completo.rename(columns={'date':'Fecha','total_pediatric_patients_hospitalized_confirmed_covid':'Total_confirmados_pediatricos','total_adult_patients_hospitalized_confirmed_covid':'Total_confirmados_adultos'}, inplace=True)
df_completo['Total_confirmados_pediatricos'].fillna(0,inplace=True)
df_completo['Total_confirmados_adultos'].fillna(0,inplace=True)

df_completo.rename(columns={'staffed_icu_adult_patients_confirmed_covid':'Total_confirmados_adultos_ICU','staffed_icu_pediatric_patients_confirmed_covid':'Total_confirmados_pediatricos_ICU'}, inplace=True)
df_completo['Total_confirmados_pediatricos_ICU'].fillna(0)
df_completo['Total_confirmados_pediatricos_ICU'].astype(float)
df_completo['Total_confirmados_adultos_ICU'].fillna(0)
df_completo['Total_confirmados_adultos_ICU'].astype(float)
df_completo['Total_confirmados_UCI'] = df_completo['Total_confirmados_pediatricos_ICU']+ df_completo['Total_confirmados_adultos_ICU']
df_completo['Total hospitalizados'] = df_completo['Total_confirmados_pediatricos'
            ]+ df_completo['Total_confirmados_adultos']

enfermos_tot =df_completo.groupby(['Fecha'])[['Total hospitalizados']].sum()
#Muertes nivel nacional
df_completo.rename(columns={'deaths_covid':'Muertes por covid-19'},inplace=True)
df_completo['Muertes por covid-19'].fillna(0)
df_completo['Muertes por covid-19'].astype(float)
muertes_tot =df_completo.groupby(['Fecha'])[['Muertes por covid-19']].sum()
muertes_tot['Muertes por covid-19'] = round((muertes_tot['Muertes por covid-19']),0)
st.markdown('## Total de hospitalizados por covid-19') 
fig2 = px.line(enfermos_tot,x=enfermos_tot.index, y = enfermos_tot['Total hospitalizados'])                     
st.plotly_chart(fig2)
st.markdown('## Muertes ocasionadas por covid-19')
fig1 = px.line(muertes_tot, x= muertes_tot.index, y = muertes_tot['Muertes por covid-19'])
fig1.update_traces(line_color = "#A20A0A")
st.plotly_chart(fig1)