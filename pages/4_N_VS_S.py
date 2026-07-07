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

import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 레이아웃 설정
st.set_page_config(page_title="N vs S 성향 비교", layout="wide")

# 데이터 불러오기
try:
    df = pd.read_csv('countries_mbti.csv')
    mbti_cols = [col for col in df.columns if col != 'Country']
    
    st.title("🔮 전 세계 N(직관형) vs S(감각형) 최종 비율 비교")
    st.markdown("전 세계 모든 국가의 데이터를 합산하여 **N(두 번째 글자가 N인 유형)**과 **S(두 번째 글자가 S인 유형)**의 최종 비율을 비교합니다.")
    st.write("---")

    # N과 S에 해당하는 열 분류
    n_cols = [col for col in mbti_cols if col[1] == 'N']
    s_cols = [col for col in mbti_cols if col[1] == 'S']

    # 전 세계 평균 데이터 계산
    global_n = df[n_cols].sum(axis=1).mean()
    global_s = df[s_cols].sum(axis=1).mean()

    # 비율 백분율(%) 변환 및 정규화
    total_ns = global_n + global_s
    global_n_pct = (global_n / total_ns) * 100
    global_s_pct = (global_s / total_ns) * 100

    # 1) 숫자로 확실하게 딱 나눠서 한눈에 보기 (Metric)
    # 안전하게 Streamlit 고유 내장 기능만 사용하여 에러를 방지합니다.
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌌 직관형 (N)")
        st.metric(label="전 세계 총 비율", value=f"{global_n_pct:.2f}%")
        
    with col2:
        st.subheader("📐 감각형 (S)")
        st.metric(label="전 세계 총 비율", value=f"{global_s_pct:.2f}%")

    st.write("---")

    # 2) 시각적 확인을 위한 도넛 차트
    df_global_ns = pd.DataFrame({
        "성향": ["N (직관형)", "S (감각형)"],
        "비율": [global_n_pct, global_s_pct]
    })

    fig_ns = px.pie(df_global_ns, values='비율', names='성향', 
                    hole=0.45, 
                    color_discrete_sequence=['#9467bd', '#2ca02c'])
    fig_ns.update_traces(textposition='inside', textinfo='percent+label', textfont_size=16)
    st.plotly_chart(fig_ns, use_container_width=True)

except FileNotFoundError:
    st.error("❌ `countries_mbti.csv` 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
