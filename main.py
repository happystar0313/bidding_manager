import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="클레버디 입찰관리 시스템", layout="wide")

# 프로젝트 목록을 불러오는 함수
def get_data_file(year):
    return f"bidding_data_{year}.csv"

# 목록 조회에 사용할 형식 변환 함수
def load_recent_data():
    recent_bids = []
    recent_openings = []
    current_year = datetime.now().year

    for year in range(current_year - 1, current_year + 1):
        file_path = get_data_file(year)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = df.fillna("")
            if not df.empty:
                if "입찰명" in df.columns and "공고일" in df.columns:
                    recent_bids.extend(df[["입찰명", "공고일"]].dropna().tail(3).values.tolist())
                if "입찰명" in df.columns and "낙찰업체" in df.columns:
                    opened = df[df["낙찰업체"].str.strip() != ""]
                    recent_openings.extend(opened[["입찰명", "낙찰업체"]].tail(3).values.tolist())

    return recent_bids, recent_openings

# 목록 불러오기
recent_bids, recent_openings = load_recent_data()
current_year = datetime.now().year

# 로고 표시
logo_path = "로고.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=250)
else:
    st.image("https://via.placeholder.com/250x100?text=Clever:D", width=250)

st.markdown("<h1 style='text-align: center;'>🏛️ 클레버디 입찰관리 시스템</h1>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("## 📂 메뉴")

if st.button("📝 입찰정보 입력"):
    st.switch_page("pages/bidding_entry.py")
if st.button("📊 개찰정보 입력"):
    st.switch_page("pages/bidding_opening.py")
if st.button("📜 입찰정보 조회"):
    st.switch_page("pages/bidding_list.py")
if st.button("🏆 개찰 결과 확인"):
    st.switch_page("pages/bidding_results.py")

st.markdown("---")

# 처리된 목록 표시
st.markdown("### 📌 최근 등록된 입찰")
if recent_bids:
    for bid in recent_bids:
        bid_name, bid_date = bid[0], bid[1]
        if st.button(f"📄 {bid_name} (공고일: {bid_date})", key=f"bid_{bid_name}"):
            st.experimental_set_query_params(bid=bid_name)
            st.switch_page("pages/bidding_list.py")
else:
    st.markdown("📭 최근 등록된 입찰이 없습니다.")

st.markdown("---")

st.markdown("### 🏆 최근 개찰 완료된 입찰")
if recent_openings:
    for opening in recent_openings:
        opening_name, winner = opening[0], opening[1]
        if st.button(f"🏅 {opening_name} → 낙찰업체: {winner}", key=f"open_{opening_name}"):
            st.experimental_set_query_params(bid=opening_name)
            st.switch_page("pages/bidding_results.py")
else:
    st.markdown("📭 최근 개찰된 입찰이 없습니다.")

st.markdown("---")
st.markdown(f"© 2025 클레버디 | 입찰관리 시스템 v1.0 | 📅 현재 연도: **{current_year}년**")
