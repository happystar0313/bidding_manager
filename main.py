import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="🏠 입찰관리 시스템 v1.0", layout="wide")

st.title("🏠 클레버디 입찰관리 시스템")

# 현재 연도 기준 최근 입찰 데이터 로드
current_year = datetime.now().year

# 파일 경로 함수
def get_data_file(year):
    return f"bidding_data_{year}.csv"

# 최근 데이터 불러오기
def load_recent_data():
    recent_bids = []
    recent_openings = []
    for year in range(current_year - 1, current_year + 1):
        path = get_data_file(year)
        if os.path.exists(path):
            df = pd.read_csv(path).fillna("")
            if not df.empty:
                if "입찰명" in df.columns and "공고일" in df.columns:
                    recent_bids.extend(df[["입찰명", "공고일"]].dropna().tail(3).values.tolist())
                if "입찰명" in df.columns and "낙찰업체" in df.columns:
                    opened = df[df["낙찰업체"].str.strip() != ""]
                    recent_openings.extend(opened[["입찰명", "낙찰업체"]].tail(3).values.tolist())
    return recent_bids, recent_openings

# 로고 출력
logo_path = "로고.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=250)
else:
    st.image("https://via.placeholder.com/250x100?text=Clever:D", width=250)

st.markdown("---")

st.markdown("## 📋 메뉴")

col1, col2 = st.columns(2)

with col1:
    if st.button("📥 입찰정보 입력"):
        st.switch_page("pages/bidding_entry.py")
    if st.button("📤 개찰정보 입력"):
        st.switch_page("pages/bidding_opening.py")

with col2:
    if st.button("📄 입찰정보 조회"):
        st.switch_page("pages/bidding_list.py")
    if st.button("🏆 개찰결과 확인"):
        st.switch_page("pages/bidding_results.py")

st.markdown("---")

# 최근 입찰 및 개찰 정보
recent_bids, recent_openings = load_recent_data()

st.markdown("### 🕑 최근 등록된 입찰")
if recent_bids:
    for bid_name, bid_date in recent_bids:
        encoded_bid = urllib.parse.quote(bid_name)
        st.markdown(f"[📄 {bid_name} (공고일: {bid_date})](./pages/bidding_list.py?bid={encoded_bid})", unsafe_allow_html=True)
else:
    st.markdown("❗ 최근 등록된 입찰이 없습니다.")

st.markdown("---")

st.markdown("### 🏁 최근 개찰 완료된 입찰")
if recent_openings:
    for bid_name, winner in recent_openings:
        encoded_bid = urllib.parse.quote(bid_name)
        st.markdown(f"[🏆 {bid_name} → 낙찰업체: {winner}](./pages/bidding_results.py?bid={encoded_bid})", unsafe_allow_html=True)
else:
    st.markdown("❗ 최근 개찰된 입찰이 없습니다.")

st.markdown("---")
st.markdown(f"© {current_year} 클레버디 | 입찰관리 시스템 v1.0")
