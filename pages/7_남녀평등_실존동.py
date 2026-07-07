import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="성비 균형 동 TOP 5", layout="wide")

st.title("⚖️ 남녀평등 실존동: 성비 균형 TOP 5")
st.markdown("안산에서 남성과 여성의 비율이 가장 50:50에 가깝고 균형 잡힌 동 TOP 5를 선정합니다.")
st.write("---")

try:
    df = pd.read_csv('population.csv')
    
    # 연도 선택
    years = sorted(list(set([int(col.split('년')[0]) for col in df.columns if '년_총인구수' in col])))
    selected_year = st.selectbox("📅 분석할 연도를 선택하세요:", years, index=len(years)-1)
    
    # 선택 연도의 남/여 인구 컬럼 정의
    total_col = f"{selected_year}년_총인구수"
    male_col = f"{selected_year}년_남자 인구수"
    female_col = f"{selected_year}년_여자 인구수"
    
    df_gender = df[['행정구역(동)', total_col, male_col, female_col]].copy()
    
    # 인구가 0인 동 예외 처리 및 비율 계산
    df_gender = df_gender[df_gender[total_col] > 0]
    df_gender['남성비율'] = (df_gender[male_col] / df_gender[total_col]) * 100
    df_gender['여성비율'] = (df_gender[female_col] / df_gender[total_col]) * 100
    
    # 50%에서 벗어난 절대값(차이) 계산 -> 이 차이가 작을수록 평등함
    df_gender['성비차이'] = (df_gender['남성비율'] - 50).abs()
    
    # 성비 차이가 가장 작은 TOP 5 동 추출
    top_5_balanced = df_gender.sort_values(by='성비차이').head(5).reset_index(drop=True)
    
    st.subheader(f"🏆 {selected_year}년 성비 균형이 가장 완벽한 동 TOP 5")
    
    # 리스트 나열
    for idx, row in top_5_balanced.iterrows():
        st.write(f"**{idx+1}위: {row['행정구역(동)']}** (남성 {row['남성비율']:.2f}% : 여성 {row['여성비율']:.2f}%)")
        
    st.write("---")
    
    # 시각화용 데이터 변형 (Melt)
    df_melted = top_5_balanced.melt(
        id_vars=['행정구역(동)'], 
        value_vars=['남성비율', '여성비율'], 
        var_name='성별', 
        value_name='비율(%)'
    )
    
    # 바 차트 생성 (bgroupmode -> barmode로 수정 완료)
    fig = px.bar(
        df_melted, 
        x='행정구역(동)', 
        y='비율(%)', 
        color='성별', 
        barmode='group', # 👈 이 부분의 오타를 올바르게 고쳤습니다.
        title=f"{selected_year}년 성비 평등 TOP 5 동의 남녀 비율 비교 (50%에 가까울수록 평등)",
        labels={'비율(%)': '인구 비율 (%)', '행정구역(동)': '행정동'},
        color_discrete_map={'남성비율': '#3498db', '여성비율': '#e74c3c'}
    )
    
    # 기준선(50%) 표시
    fig.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Ideal 50%")
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("❌ `population.csv` 파일을 찾을 수 없습니다.")
