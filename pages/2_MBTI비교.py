import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MBTI별 국가 비교", layout="wide")

st.title("🔍 MBTI 유형별 국가 비교")

try:
    df = pd.read_csv('countries_mbti.csv')
    
    # MBTI 유형 선택 (Country 열 제외)
    mbti_types = [col for col in df.columns if col != 'Country']
    selected_mbti = st.selectbox("비교할 MBTI 유형을 선택하세요:", sorted(mbti_types))
    
    # 해당 MBTI를 기준으로 정렬 후 상위/하위 국가 추출 수 설정
    top_n = st.slider("표시할 국가 수를 선택하세요:", min_value=5, max_value=30, value=15)
    
    # 데이터 정렬
    mbti_df = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False)
    
    st.subheader(f"👑 {selected_mbti} 유형 비율이 높은 국가 Top {top_n}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 상위 N개국 차트 시각화
        top_df = mbti_df.head(top_n)
        fig = px.bar(top_df, x='Country', y=selected_mbti,
                     title=f"국가별 {selected_mbti} 비율 순위",
                     labels={selected_mbti: '비율', 'Country': '국가'},
                     color=selected_mbti, color_continuous_scale='Purples')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown(f"**📊 {selected_mbti} 비율이 가장 높은 5개국**")
        for idx, row in mbti_df.head(5).reset_index().iterrows():
            st.write(f"{idx+1}위: **{row['Country']}** ({row[selected_mbti]*100:.2f}%)")
            
        st.write("---")
        st.markdown(f"**📉 {selected_mbti} 비율이 가장 낮은 5개국**")
        for idx, row in mbti_df.tail(5).iloc[::-1].reset_index().iterrows():
            st.write(f"뒤에서 {idx+1}위: **{row['Country']}** ({row[selected_mbti]*100:.2f}%)")

except FileNotFoundError:
    st.error("❌ `countries_mbti.csv` 파일을 찾을 수 없습니다.")
