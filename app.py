import streamlit as st
import pandas as pd
import plotly.express as px
import requests

@st.cache
def load_data():
    r = requests.get('https://coronavirus-19-api.herokuapp.com/countries')
    df = pd.DataFrame.from_dict(r.json()) if r.status_code == 200 else pd.read_csv('data.csv')
    return df[df.country != 'World']

df = load_data()

st.sidebar.title('Corona Dashboard')
st.sidebar.markdown('by Paul-Louis Proeve')
st.sidebar.markdown('[Code on Github](https://github.com/pietz/covid19-dashboard)')
st.sidebar.markdown('---')

regions = ['world', 'europe', 'asia', 'africa', 'north america', 'south america']
region = st.sidebar.selectbox('Select a region for the map', regions, regions.index('world'))
col = st.sidebar.selectbox('Select the attribute of interest', df.columns[1:])
st.sidebar.markdown('---')

txt = 'There have been a total of ' + str(df.cases.sum()) + ' COVID-19 cases worldwide'
txt += ' resulting in ' + str(df.deaths.sum()) + ' deaths.'
st.sidebar.markdown(txt)

cp = px.choropleth(df, locations='country', locationmode='country names', color=col, scope=region)
st.plotly_chart(cp, use_container_width=True)

df_bar = df.sort_values(col, ascending=False)[:10]
bc = px.bar(df_bar, 'country', col, color=col)
st.plotly_chart(bc, use_container_width=True)