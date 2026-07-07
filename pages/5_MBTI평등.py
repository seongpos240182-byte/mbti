import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("⚖️ MBTI 분포가 가장 균형 잡힌 나라 TOP 15")

df = pd.read_csv('countries_mbti.csv')
mbti_cols = [col for col in df.columns if col != 'Country']

df['Standard_Deviation'] = df[mbti_cols].std(axis=1)
top_15_balanced = df.sort_values(by='Standard_Deviation', ascending=True).head(15)

fig = px.bar(top_15_balanced, x='Country', y='Standard_Deviation', title="MBTI 평등 국가 15", color='Standard_Deviation', color_continuous_scale='Greens_r')
st.plotly_chart(fig, use_container_width=True)
