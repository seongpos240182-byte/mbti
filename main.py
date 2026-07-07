import streamlit as pd
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="국가별 MBTI 분석 대시보드", layout="wide")

st.title("🌍 국가별 MBTI 분포 데이터 분석")
st.markdown("""
이 대시보드는 전 세계 국가들의 MBTI 유형별 분포 데이터를 시각화하고 분석하는 도구입니다.
왼쪽 사이드바의 메뉴를 이용해 원하는 분석 페이지로 이동할 수 있습니다.
""")

# 데이터 불러오기
try:
    df = pd.read_csv('countries_mbti.csv')
    
    st.subheader("📊 데이터셋 개요")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 국가 수", f"{len(df)}개국")
    col2.metric("분석된 MBTI 유형", f"{len(df.columns) - 1}개")
    col3.metric("데이터 출처", "사용자 업로드 파일 (countries_mbti.csv)")

    st.subheader("👀 데이터 미리보기 (상위 5개국)")
    st.dataframe(df.head(), use_container_width=True)
    
    st.subheader("💡 페이지 안내")
    st.markdown("""
    - **국가별 MBTI**: 특정 국가를 선택하여 해당 국가 내에서 어떤 MBTI 유형이 가장 높은 비율을 차지하는지 차트로 확인합니다.
    - **MBTI 비교**: 특정 MBTI 유형을 선택하여 해당 유형의 비율이 가장 높은 국가부터 낮은 국가까지 순위를 비교합니다.
    """)

except FileNotFoundError:
    st.error("❌ `countries_mbti.csv` 파일을 찾을 수 없습니다. 파일이 올바른 위치에 있는지 확인해주세요.")
