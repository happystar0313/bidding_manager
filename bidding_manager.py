import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="📋 입찰 관리 매니저", layout="wide")

st.title("📋 입찰 통합 데이터 관리")

# ✅ 연도별 데이터 파일 경로 함수
def get_data_file(year):
    return f"bidding_data_{year}.csv"

# ✅ 데이터 로드 함수
def load_data(year):
    file_path = get_data_file(year)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

# ✅ 연도 선택
year = st.selectbox("📅 연도 선택", ["2024", "2025", "2026", "2027"])
df = load_data(year)

if df.empty:
    st.warning(f"⚠ {year}년의 입찰 데이터가 없습니다.")
else:
    st.success(f"✅ {year}년 입찰 데이터 {len(df)}건 불러오기 성공!")

    # ✅ 데이터 편집 테이블
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    # ✅ 저장 버튼
    if st.button("💾 변경사항 저장"):
        file_path = get_data_file(year)
        edited_df.to_csv(file_path, index=False)
        st.success("변경사항이 저장되었습니다!")
