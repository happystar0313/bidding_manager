import streamlit as st
import pandas as pd
import os
from urllib.parse import unquote

st.set_page_config(page_title="🏆 개찰정보 조회", layout="wide")

st.title("🏆 개찰정보 조회")

# ✅ URL에서 입찰명 가져오기
query_params = st.query_params
selected_bid = query_params.get("bid", [""])[0]
selected_bid = unquote(selected_bid)  # URL 디코딩

# ✅ 데이터 파일 경로 함수
def get_data_file(year):
    return f"bidding_data_{year}.csv"

# ✅ 데이터 불러오기
current_year = 2025  # 기본 연도 설정
bidding_data = []

for year in range(current_year - 1, current_year + 1):
    file_path = get_data_file(year)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = df.fillna("")
        bidding_data.append(df)

# ✅ 데이터 합치기
if bidding_data:
    df_all = pd.concat(bidding_data, ignore_index=True)
else:
    df_all = pd.DataFrame()

# ✅ 특정 입찰명으로 필터링
if selected_bid and not df_all.empty:
    df_filtered = df_all[df_all["입찰명"] == selected_bid]
    if not df_filtered.empty:
        st.write(df_filtered)
    else:
        st.warning(f"⚠ '{selected_bid}'에 대한 개찰 정보가 없습니다.")
else:
    st.warning("📭 특정 개찰 정보를 조회하려면 목록에서 클릭하세요.")
