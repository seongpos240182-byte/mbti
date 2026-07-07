import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 MBTI 현황", layout="wide")

st.title("📍 국가별 MBTI 현황 분석")

try:
    df = pd.read_csv('countries_mbti.csv')
    
    # 국가 선택 사이드바/드롭다운
    countries = df['Country'].unique()
    selected_country = st.selectbox("분석할 국가를 선택하세요:", sorted(countries))
    
    # 선택된 국가의 데이터 추출
    country_data = df[df['Country'] == selected_country].drop(columns=['Country']).T
    country_data.columns = ['Ratio']
    country_data = country_data.reset_index().rename(columns={'index': 'MBTI'})
    
    # 비율이 높은 순으로 정렬
    country_data = country_data.sort_values(by='Ratio', ascending=False)
    
    # 시각화 및 정보 제공
    st.subheader(f"✨ {selected_country}의 MBTI 분포")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Plotly 바 차트 생성
        fig = px.bar(country_data, x='MBTI', y='Ratio', 
                     title=f"{selected_country} MBTI 유형별 비율",
                     labels={'Ratio': '비율', 'MBTI': 'MBTI 유형'},
                     color='Ratio', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown(f"**🔝 {selected_country}에서 가장 많은 유형 TOP 3**")
        for i, row in country_data.head(3).iterrows():
            st.write(f"{i+1}위: **{row['MBTI']}** ({row['Ratio']*100:.2f}%)")
            
        st.write("---")
        st.markdown("**📄 전체 데이터 테이블**")
        st.dataframe(country_data.reset_index(drop=True), use_container_width=True)

except FileNotFoundError:
    st.error("❌ `countries_mbti.csv` 파일을 찾을 수 없습니다.")
