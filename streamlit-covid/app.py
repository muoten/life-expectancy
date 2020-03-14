import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import requests
import requests_cache

import plotly.express as px

st.title('Covid-19')

st.markdown('## Number of cases and deaths per country')
st.markdown('Source: https://www.worldometers.info/coronavirus/#countries')
st.markdown('*Note: number of cases depends on the testing protocol*')

URL="https://www.worldometers.info/coronavirus/#countries"
requests_cache.install_cache('demo_cache', expire_after=600)
myhtml = requests.get(URL)
df_html=pd.read_html(myhtml.text)[0]

st.write(df_html)

st.markdown('## Test rates per country.')
st.image('https://i.dailymail.co.uk/1s/2020/03/12/23/25900582-8106127-Pueyo_also_noted_that_the_US_needs_to_drastically_increase_the_n-a-2_1584056534751.jpg', use_column_width=True)


df_px = px.data.gapminder().query("year==2007")
df = df_html.merge(df_px, left_on='Country,Other', right_on='country')

df['Death Rate'] = df['TotalDeaths']/df['TotalCases']
df = df.fillna(0)

st.markdown('## Death rate estimates.')
st.markdown('*Note: Death rate calculated as TotalDeaths/TotalCases. Where TotalCases depends on the testing protocol and the ratio of tests performed per 1000 habitants*')


st.markdown('Colored map for countries with more than 1000 detected cases:')
df = df[df['TotalCases'] > 1000]
fig = px.choropleth(df, locations="iso_alpha",
                    color="Death Rate",
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
#fig.show()
st.write(fig)