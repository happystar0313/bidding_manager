import streamlit as st
import pandas as pd
import os
from datetime import datetime
from urllib.parse import quote

st.set_page_config(page_title="🏛️ 클레버디 입찰관리 시스템", layout="wide")

# ✅ 로고 이미지 파일 체크 후 표시
logo_path = "로고.png"

if os.path.exists(logo_path):
    st.image(logo_path, width=250)
else:
    default_logo_url = "https://via.placeholder.com/250x100?text=Clever:D"
    st.image(default_logo_url, width=250)

st.markdown("<h1 style='text-align: center;'>🏛️ 클레버디 입찰관리 시스템</h1>", unsafe_allow_html=True)

st.markdown("---")

# ✅ 현재 연도 가져오기
current_year = datetime.now().year

# ✅ 데이터 파일 경로 함수
def get_data_file(year):
    return f"bidding_data_{year}.csv"

# ✅ 최근 데이터 불러오기 함수 (입찰명 전달 가능하도록 개선)
def load_recent_data():
    recent_bids = []
    recent_openings = []
    
    for year in range(current_year - 1, current_year + 1):  # 작년~올해 데이터만 확인
        file_name = get_data_file(year)
        if os.path.exists(file_name):
            df = pd.read_csv(file_name)
            df = df.fillna("")  # ✅ NaN 값 제거

            if not df.empty:
                if "입찰명" in df.columns and "공고일" in df.columns:
                    recent_bids.extend(df[["입찰명", "공고일"]].dropna().tail(3).values.tolist())

                if "입찰명" in df.columns and "낙찰업체" in df.columns:
                    opened = df[df["낙찰업체"].str.strip() != ""]  # ✅ 빈 값 필터링
                    recent_openings.extend(opened[["입찰명", "낙찰업체"]].tail(3).values.tolist())

    return recent_bids, recent_openings

# ✅ 최근 데이터 불러오기
recent_bids, recent_openings = load_recent_data()

# ✅ 메뉴 섹션 (모바일 UI 최적화 → 세로 정렬)
st.markdown("## 📂 메뉴")

st.markdown("""
<style>
    .menu-button { 
        display: block; 
        width: 100%; 
        padding: 10px 20px; 
        text-align: center;
        font-size: 18px; 
        font-weight: bold; 
        border-radius: 10px; 
        background-color: #f8f9fa; 
        margin: 5px 0;
    }
    .menu-button:hover { background-color: #e9ecef; }
</style>
""", unsafe_allow_html=True)

if st.button("📝 입찰정보 입력", key="entry"):
    st.switch_page("pages/bidding_entry.py")
if st.button("📊 개찰정보 입력", key="opening"):
    st.switch_page("pages/bidding_opening.py")
if st.button("📜 입찰정보 조회", key="list"):
    st.switch_page("pages/bidding_list.py")
if st.button("🏆 개찰 결과 확인", key="results"):
    st.switch_page("pages/bidding_results.py")

st.markdown("---")

# ✅ 📌 "최근 등록된 입찰" (클릭하면 입찰정보 조회 + 자동 필터링)
st.markdown("### 📌 최근 등록된 입찰")
if recent_bids:
    for bid in recent_bids:
        bid_name, bid_date = bid[0], bid[1]
        bid_encoded = quote(bid_name)  # URL 인코딩
        bid_link = f"[📄 **{bid_name}** (공고일: {bid_date})](/pages/bidding_list.py?bid={bid_encoded})"
        st.markdown(bid_link, unsafe_allow_html=True)
else:
    st.markdown("📭 최근 등록된 입찰이 없습니다.")

st.markdown("---")

# ✅ 🏆 "최근 개찰 완료된 입찰" (클릭하면 개찰정보 조회 + 자동 필터링)
st.markdown("### 🏆 최근 개찰 완료된 입찰")
if recent_openings:
    for opening in recent_openings:
        opening_name, winner = opening[0], opening[1]
        opening_encoded = quote(opening_name)  # URL 인코딩
        opening_link = f"[🏅 **{opening_name}** → 낙찰업체: **{winner}**](/pages/bidding_results.py?bid={opening_encoded})"
        st.markdown(opening_link, unsafe_allow_html=True)
else:
    st.markdown("📭 최근 개찰된 입찰이 없습니다.")

st.markdown("---")

# ✅ 푸터에 현재 연도 배치
st.markdown(f"© 2025 클레버디 | 입찰관리 시스템 v1.0 | 📅 현재 연도: **{current_year}년**")
