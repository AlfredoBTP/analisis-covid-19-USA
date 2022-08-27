#Librerias a utilizar
import streamlit as st
import pandas as pd
import plotly.express as px


df_completo= pd.read_csv("df.csv")
df_completo = df_completo.drop_duplicates()
df_completo= df_completo.sort_values('date')
#Titulo para nuestro Dashboard
st.title("Análisis de hospitalización y mortalidad E.U.A.")

#Filtre por fecha, sustitui valores faltantes por 0 e hice cast a las columnas para sumalas
df_completo.rename(columns={'date':'Fecha','total_pediatric_patients_hospitalized_confirmed_covid':'Pediatricos confirmados','total_adult_patients_hospitalized_confirmed_covid':'Adultos confirmados'}, inplace=True)
df_completo['Pediatricos confirmados'].fillna(0,inplace=True)
df_completo['Adultos confirmados'].fillna(0,inplace=True)
df_completo.rename(columns={'staffed_icu_adult_patients_confirmed_covid':'Adultos confirmados UCI','staffed_icu_pediatric_patients_confirmed_covid':'Pediatricos confirmados UCI'}, inplace=True)
df_completo['Pediatricos confirmados UCI'].fillna(0,inplace=True)
df_completo['Adultos confirmados UCI'].fillna(0,inplace=True)

hosp_pedia=df_completo.groupby(['Fecha'])[['Pediatricos confirmados']].sum()
hosp_pediaUCI_=df_completo.groupby(['Fecha'])[['Pediatricos confirmados UCI']].sum()
hosp_adulto=df_completo.groupby(['Fecha'])[['Adultos confirmados']].sum()
hosp_adulto_UCI=df_completo.groupby(['Fecha'])[['Adultos confirmados UCI']].sum()
pedia_merge = hosp_pedia.merge(hosp_pediaUCI_, how='left', left_index=True, right_index=True)
adulto_merge = hosp_adulto.merge(hosp_adulto_UCI, how='left', left_index=True, right_index=True)

fig1 = px.line(pedia_merge, x= pedia_merge.index, y= [pedia_merge['Pediatricos confirmados'],pedia_merge['Pediatricos confirmados UCI']],width=900, height=600)
fig2 = px.line(adulto_merge, x= adulto_merge.index, y =[adulto_merge['Adultos confirmados'], adulto_merge['Adultos confirmados UCI']],width=900, height=600)

df_completo.rename(columns={'deaths_covid':'Muertes_por_covid'},inplace=True)
df_completo['Muertes_por_covid'].fillna(0,inplace=True)
df_completo['Tasa de mortalidad_UCI'] = ((100/((df_completo['Adultos confirmados UCI']) +
                                               ( df_completo['Pediatricos confirmados UCI'])))
                                                * (df_completo['Muertes_por_covid']))
df_completo['Tasa de mortalidad hospitalizados'] = ((100/((df_completo['Adultos confirmados']) +
                                               ( df_completo['Pediatricos confirmados'])+(df_completo['Adultos confirmados UCI']) +
                                               ( df_completo['Pediatricos confirmados UCI'])))
                                                * (df_completo['Muertes_por_covid']))
df_completo['Tasa de mortalidad_UCI'].fillna(0,inplace=True)

mortalidad = df_completo.groupby(['Fecha'])[['Tasa de mortalidad_UCI']].mean()
mortalidad2 = df_completo.groupby(['Fecha'])[['Tasa de mortalidad hospitalizados']].mean()
mortalidad_merge = mortalidad.merge(mortalidad2, how='left', left_index=True, right_index=True)
values= [mortalidad['Tasa de mortalidad_UCI'],mortalidad2['Tasa de mortalidad hospitalizados'] ]
fig3 = px.scatter(mortalidad_merge, x= mortalidad_merge.index.values, y = [mortalidad_merge['Tasa de mortalidad_UCI'], mortalidad_merge['Tasa de mortalidad hospitalizados']], width=900, height=600)
df_completo['adult_icu_bed_covid_utilization'].fillna(0,inplace=True)
df_completo['adult_icu_bed_covid_utilization'].astype(float)
porcentaje_camas =df_completo.groupby(['Fecha'])[['adult_icu_bed_covid_utilization']].mean()
porcentaje_camas['Promedio de % de camas UCI utilizadas'] = porcentaje_camas['adult_icu_bed_covid_utilization'] * 100
labels= porcentaje_camas.index
values= porcentaje_camas['Promedio de % de camas UCI utilizadas']
fig4 = px.line(x= labels, y = values, width=800, height=600)
st.markdown('## Pacientes pediatricos hospitalizados por covid en camas común y UCI')
st.plotly_chart(fig1)
st.markdown('## Pacientes adultos hospitalizados por covid en camas común y UCI')
st.plotly_chart(fig2)
st.markdown('## Porcentaje de camas UCI utilizadas a nivel nacional')
st.plotly_chart(fig4)
st.markdown('## Tasa de mortalidad en pacientes UCI y común')
st.plotly_chart(fig3)
