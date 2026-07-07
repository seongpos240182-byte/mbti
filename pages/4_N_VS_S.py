import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🔮 N(직관형) vs S(감각형) 비율 비교")

df = pd.read_csv('countries_mbti.csv')
mbti_cols = [col for col in df.columns if col != 'Country']
n_cols = [col for col in mbti_cols if col[1] == 'N']
s_cols = [col for col in mbti_cols if col[1] == 'S']

df_ns = df[['Country']].copy()
df_ns['N_Total'] = df[n_cols].sum(axis=1)
df_ns['S_Total'] = df[s_cols].sum(axis=1)

df_ns_melted = df_ns.melt(id_vars='Country', value_vars=['N_Total', 'S_Total'], var_name='Preference', value_name='Ratio')
fig = px.bar(df_ns_melted, x='Country', y='Ratio', color='Preference', title="전 세계 N vs S")
st.plotly_chart(fig, use_container_width=True)
