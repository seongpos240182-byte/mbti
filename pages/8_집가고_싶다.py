import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="인구 극단 TOP 3 성비 비교", layout="wide")

st.title("🏠 집가고 싶다: 인구 최다 vs 최소 동 성비 비교")
st.markdown("안산에서 인구가 가장 많은 3개 동과 가장 적은 3개 동을 뽑아, 사람이 많고 적음에 따라 성비 특징이 어떻게 다른지 비교합니다.")
st.write("---")

try:
    df = pd.read_csv('population.csv')
    
    # 연도 선택
    years = sorted(list(set([int(col.split('년')[0]) for col in df.columns if '년_총인구수' in col])))
    selected_year = st.selectbox("📅 분석할 연도를 선택하세요:", years, index=len(years)-1)
    
    total_col = f"{selected_year}년_총인구수"
    male_col = f"{selected_year}년_남자 인구수"
    female_col = f"{selected_year}년_여자 인구수"
    
    # 필요한 컬럼 정제 및 인구 0인 곳 예외 필터링
    df_data = df[['행정구역(동)', total_col, male_col, female_col]].copy()
    df_data = df_data[df_data[total_col] > 0].sort_values(by=total_col, ascending=False)
    
    # 인구 상위 3개동 & 하위 3개동 추출
    top_3 = df_data.head(3).copy()
    top_3['그룹'] = '인구 최다 TOP 3'
    
    bottom_3 = df_data.tail(3).copy()
    bottom_3['그룹'] = '인구 최소 TOP 3'
    
    # 두 그룹 합치기
    df_extreme = pd.concat([top_3, bottom_3]).reset_index(drop=True)
    
    # 성별 비율 계산
    df_extreme['남성비율'] = (df_extreme[male_col] / df_extreme[total_col]) * 100
    df_extreme['여성비율'] = (df_extreme[female_col] / df_extreme[total_col]) * 100
    
    # 화면 레이아웃 분할 배치
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔥 사람이 가장 많은 동 (TOP 3)")
        for idx, row in top_3.reset_index().iterrows():
            st.write(f"{idx+1}위: **{row['행정구역(동)']}** ({row[total_col]:,} 명)")
            
    with col2:
        st.subheader("🍃 사람이 가장 적은 동 (TOP 3)")
        for idx, row in bottom_3.iloc[::-1].reset_index().iterrows():
            st.write(f"뒤에서 {idx+1}위: **{row['행정구역(동)']}** ({row[total_col]:,} 명)")
            
    st.write("---")
    
    # 시각화 데이터 변환 (Melt)
    df_melted = df_extreme.melt(
        id_vars=['행정구역(동)', '그룹'], 
        value_vars=['남성비율', '여성비율'], 
        var_name='성별', 
        value_name='비율(%)'
    )
    
    # 시각화 그리기: Stacked Bar Chart 활용하여 100% 비율 채우기
    fig = px.bar(
        df_melted, 
        x='행정구역(동)', 
        y='비율(%)', 
        color='성별',
        facet_col='그룹', # 그룹별로 그래프 구역을 나눔
        category_orders={"그룹": ["인구 최다 TOP 3", "인구 최소 TOP 3"]},
        title=f"{selected_year}년 인구 극단 동별 남녀 성비 구성 비교 그래프",
        labels={'비율(%)': '성비 비율 (%)', '행정구역(동)': '행정동'},
        color_discrete_map={'남성비율': '#2ecc71', '여성비율': '#9b59b6'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("❌ `population.csv` 파일을 찾을 수 없습니다.")
