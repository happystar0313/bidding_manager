import streamlit as st
import pandas as pd
import os
from urllib.parse import unquote

st.set_page_config(page_title="입찰정보 조회", layout="wide")

st.title("📜 입찰정보 조회")

# ✅ URL에서 입찰명 가져오기
query_params = st.query_params
selected_bid = query_params.get("bid", [""])[0]
selected_bid = unquote(selected_bid)  # URL 디코딩

st.write(f"📌 선택된 입찰명: {selected_bid}")  # ✅ 입찰명이 정상적으로 넘어오는지 확인

# ✅ 데이터 파일 경로 함수
def get_data_file(year):
    return f"bidding_data_{year}.csv"

# ✅ 데이터 불러오기
current_year = 2025
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

st.write("📂 불러온 데이터 (첫 5개):", df_all.head())  # ✅ 데이터가 정상적으로 불러와지는지 확인

# ✅ 특정 입찰명으로 필터링
if selected_bid and not df_all.empty and "입찰명" in df_all.columns:
    df_filtered = df_all[df_all["입찰명"] == selected_bid]
    st.write("🔍 필터링된 데이터:", df_filtered)  # ✅ 필터링 결과 확인
