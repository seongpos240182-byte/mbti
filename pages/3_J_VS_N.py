import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("⚖️ J(판단형) vs P(인식형) 비율 비교")

df = pd.read_csv('countries_mbti.csv')
mbti_cols = [col for col in df.columns if col != 'Country']
j_cols = [col for col in mbti_cols if col.endswith('J')]
p_cols = [col for col in mbti_cols if col.endswith('P')]

df_jp = df[['Country']].copy()
df_jp['J_Total'] = df[j_cols].sum(axis=1)
df_jp['P_Total'] = df[p_cols].sum(axis=1)

df_jp_melted = df_jp.melt(id_vars='Country', value_vars=['J_Total', 'P_Total'], var_name='Preference', value_name='Ratio')
fig = px.bar(df_jp_melted, x='Country', y='Ratio', color='Preference', title="전 세계 J vs P")
st.plotly_chart(fig, use_container_width=True)
