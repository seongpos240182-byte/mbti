import streamlit as st
import pandas as pd

st.set_page_config(page_title="우리 동네 인구 순위", layout="wide")

st.title("🥇 수준을 알라: 안산시 동별 인구 순위")
st.markdown("내가 사는 동을 선택하면 안산시 전체 동 중에서 몇 위를 차지하고 있는지 확인합니다.")
st.write("---")

try:
    # 데이터 불러오기
    df = pd.read_csv('population.csv')
    
    # 1. 연도 선택 (2016 ~ 2025)
    years = sorted(list(set([int(col.split('년')[0]) for col in df.columns if '년_총인구수' in col])))
    selected_year = st.selectbox("📅 분석할 연도를 선택하세요:", years, index=len(years)-1)
    
    # 2. 행정동 선택
    dongs = sorted(df['행정구역(동)'].unique())
    selected_dong = st.selectbox("🏠 우리 동(행정동)을 선택하세요:", dongs)
    
    # 선택 연도의 데이터 정렬 및 순위 매기기
    target_col = f"{selected_year}년_총인구수"
    df_rank = df[['행정구역(동)', target_col]].copy()
    df_rank['순위'] = df_rank[target_col].rank(ascending=False, method='min').astype(int)
    df_rank = df_rank.sort_values(by='순위').reset_index(drop=True)
    
    # 선택한 동의 순위 및 인구 추출
    dong_info = df_rank[df_rank['행정구역(동)'] == selected_dong].iloc[0]
    total_dongs = len(df_rank)
    
    # 결과 상단 카드 시각화
    st.subheader(f"✨ {selected_year}년 기준 [{selected_dong}]의 인구 체급")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🏆 안산시 내 인구 순위", value=f"{dong_info['순위']}위", delta=f"전체 {total_dongs}개 동 중")
    with col2:
        st.metric(label="👥 총 인구수", value=f"{dong_info[target_col]:,} 명")
        
    st.write("---")
    
    # 3. 전체 순위표 제공
    st.markdown(f"### 📊 {selected_year}년 안산시 전체 동별 인구 순위표")
    df_rank_display = df_rank.rename(columns={target_col: '총 인구수(명)'})
    
    # 내가 선택한 동을 강조하기 위한 스타일 적용 데이터프레임
    def highlight_selected(row):
        return ['background-color: #e0f7fa' if row['행정구역(동)'] == selected_dong else '' for _ in row]
    
    st.dataframe(df_rank_display.style.apply(highlight_selected, axis=1), use_container_width=True)

except FileNotFoundError:
    st.error("❌ `population.csv` 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
