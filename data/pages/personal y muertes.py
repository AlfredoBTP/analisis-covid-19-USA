#Librerias a utilizar
from pickle import TRUE
from re import T
import streamlit as st
import pandas as pd
import plotly.express as px


df_completo= pd.read_csv("df.csv")
df_completo = df_completo.drop_duplicates()
#Titulo para nuestro Dashboard
st.title("Relación entre falta de personal y la tasa de mortalidad.")
df_completo.rename(columns={'total_pediatric_patients_hospitalized_confirmed_covid':'Total_confirmados_pediatricos','total_adult_patients_hospitalized_confirmed_covid':'Total_confirmados_adultos'}, inplace=True)
df_completo['Total_confirmados_pediatricos'].fillna(0,inplace=True)
df_completo['Total_confirmados_adultos'].fillna(0,inplace=True)
df_completo.rename(columns={'staffed_icu_adult_patients_confirmed_covid':'Total_confirmados_adultos_ICU','staffed_icu_pediatric_patients_confirmed_covid':'Total_confirmados_pediatricos_ICU'}, inplace=True)
df_completo['Total_confirmados_pediatricos_ICU'].fillna(0,inplace=True)
df_completo['Total_confirmados_adultos_ICU'].fillna(0,inplace=True)
hosp_pedia=df_completo.groupby(['date'])[['Total_confirmados_pediatricos']].sum()
hosp_pediaUCI_=df_completo.groupby(['date'])[['Total_confirmados_pediatricos_ICU']].sum()
hosp_adulto=df_completo.groupby(['date'])[['Total_confirmados_adultos']].sum()
hosp_adulto_UCI=df_completo.groupby(['date'])[['Total_confirmados_adultos_ICU']].sum()
df_completo['critical_staffing_shortage_today_yes'].fillna(0,inplace=True)
df_completo['critical_staffing_shortage_today_no'].fillna(0,inplace=True)
df_completo['Porcentaje de hospitales con falta de personal'] = (100/((df_completo['critical_staffing_shortage_today_yes'])+(df_completo['critical_staffing_shortage_today_no'])))*(df_completo['critical_staffing_shortage_today_yes'])
falta_personal= df_completo.groupby('date')[['Porcentaje de hospitales con falta de personal']].mean()
df_completo.rename(columns={'deaths_covid':'Muertes_por_covid'},inplace=True)
df_completo['Muertes_por_covid'].fillna(0,inplace=True)
df_completo['Muertes_por_covid'].astype(float)
df_completo['Tasa de mortalidad_UCI'] = ((100/((df_completo['Total_confirmados_adultos_ICU']) +
                                               ( df_completo['Total_confirmados_pediatricos_ICU'])))
                                                * (df_completo['Muertes_por_covid']))
df_completo['Tasa de mortalidad hospitalizados'] = ((100/((df_completo['Total_confirmados_adultos']) +
                                               ( df_completo['Total_confirmados_pediatricos'])+(df_completo['Total_confirmados_adultos_ICU']) +
                                               ( df_completo['Total_confirmados_pediatricos_ICU'])))
                                                * (df_completo['Muertes_por_covid']))

mortalidad = df_completo.groupby(['date'])[['Tasa de mortalidad_UCI']].mean()
mortalidad2 = df_completo.groupby(['date'])[['Tasa de mortalidad hospitalizados']].mean()
mortalidad_merge = mortalidad.merge(mortalidad2, how='left', left_index=True, right_index=True)
merge = mortalidad_merge.merge(falta_personal,how='left', left_index=True, right_index=True)

fig2 = px.scatter(merge, x= merge.index, y = [merge['Tasa de mortalidad_UCI'],merge
                ['Tasa de mortalidad hospitalizados'],merge['Porcentaje de hospitales con falta de personal'] 
                ], width=1000, height=600)
fig1 = px.bar(x = falta_personal.index, y =falta_personal['Porcentaje de hospitales con falta de personal'],width=800, height=600 )
st.markdown('## Porcentajes de tasas de mortalidad y hospitales con falta de personal')
st.plotly_chart(fig2)
st.markdown('## Porcentaje de hospitales con falta de personal')
st.plotly_chart(fig1)
