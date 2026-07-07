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

import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 레이아웃 설정
st.set_page_config(page_title="J vs P 성향 비교", layout="wide")

# 데이터 불러오기
try:
    df = pd.read_csv('countries_mbti.csv')
    mbti_cols = [col for col in df.columns if col != 'Country']
    
    st.title("⚖️ 전 세계 J(판단형) vs P(인식형) 최종 비율 비교")
    st.markdown("전 세계 모든 국가의 데이터를 합산하여 **J(끝자리가 J로 끝나는 유형)**와 **P(끝자리가 P로 끝나는 유형)**의 최종 비율을 비교합니다.")
    st.write("---")

    # J와 P에 해당하는 열 분류
    j_cols = [col for col in mbti_cols if col.endswith('J')]
    p_cols = [col for col in mbti_cols if col.endswith('P')]

    # 전 세계 평균 데이터 계산
    global_j = df[j_cols].sum(axis=1).mean()
    global_p = df[p_cols].sum(axis=1).mean()

    # 비율 백분율(%) 변환 및 정규화
    total_jp = global_j + global_p
    global_j_pct = (global_j / total_jp) * 100
    global_p_pct = (global_p / total_jp) * 100

    # 1) 숫자로 확실하게 딱 나눠서 한눈에 보기 (Metric)
    # 안전하게 Streamlit 고유 내장 기능만 사용하여 에러를 방지합니다.
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📌 판단형 (J)")
        st.metric(label="전 세계 총 비율", value=f"{global_j_pct:.2f}%")
        
    with col2:
        st.subheader("📑 인식형 (P)")
        st.metric(label="전 세계 총 비율", value=f"{global_p_pct:.2f}%")

    st.write("---")

    # 2) 시각적 확인을 위한 도넛 차트
    df_global_jp = pd.DataFrame({
        "성향": ["J (판단형)", "P (인식형)"],
        "비율": [global_j_pct, global_p_pct]
    })

    fig_jp = px.pie(df_global_jp, values='비율', names='성향', 
                    hole=0.45, 
                    color_discrete_sequence=['#1f77b4', '#ff7f0e'])
    fig_jp.update_traces(textposition='inside', textinfo='percent+label', textfont_size=16)
    st.plotly_chart(fig_jp, use_container_width=True)

except FileNotFoundError:
    st.error("❌ `countries_mbti.csv` 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
