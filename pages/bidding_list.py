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

# ✅ 네 기존 UI 유지하면서 "선택된 입찰명" 조회 추가
st.markdown("## 📋 입찰 목록")

if not df_all.empty:
    st.dataframe(df_all[["입찰공고번호", "입찰명", "공고일", "마감일"]])

    # ✅ 특정 입찰명 자동 조회 추가
    if selected_bid:
        df_filtered = df_all[df_all["입찰명"] == selected_bid]
        if not df_filtered.empty:
            bid_info = df_filtered.iloc[0]  # ✅ 첫 번째 데이터 가져오기

            st.markdown("---")
            st.markdown("### 📌 선택된 입찰 정보")
            st.write(f"**📝 입찰명:** {bid_info['입찰명']}")
            st.write(f"**📅 공고일:** {bid_info['공고일']}")
            st.write(f"**⏳ 마감일:** {bid_info['마감일']}")
            st.write(f"**🏢 발주 기관:** {bid_info['발주기관']}")
            st.write(f"**💰 사업 예산:** {int(bid_info['사업예산']):,} 만원")
            st.write(f"**📑 입찰 방식:** {bid_info['입찰방식']}")
        else:
            st.warning(f"⚠ '{selected_bid}'에 대한 입찰 정보가 없습니다.")
else:
    st.warning("📭 등록된 입찰이 없습니다.")
