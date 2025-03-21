import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="🏛️ 클레버디 입찰관리 시스템", layout="wide")

# ✅ 로고 이미지 파일 체크 후 표시
logo_path = "로고.png"

if os.path.exists(logo_path):
    st.image(logo_path, width=250)
else:
    default_logo_url = "https://via.placeholder.com/250x100?text=Clever:D"
    st.image(default_logo_url, width=250)

st.title("🏛️ 클레버디 입찰관리 시스템")

st.markdown("---")

# ✅ 현재 연도 가져오기
current_year = datetime.now().year

# ✅ 데이터 파일 경로 함수
def get_data_file(year):
    return f"bidding_data_{year}.csv"

# ✅ 최근 데이터 불러오기 함수 (오류 수정)
def load_recent_data():
    recent_bids = []
    recent_openings = []
    
    for year in range(current_year - 1, current_year + 1):  # 작년, 올해 데이터만 확인
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

# ✅ 메뉴 섹션 (아이콘 중복 해결 + 폰트 크기 유지)
st.markdown("## 📂 메뉴")

col1, col2 = st.columns(2)

with col1:
    if st.button("📝 입찰정보 입력"):
        st.switch_page("pages/bidding_entry.py")
    if st.button("📊 개찰정보 입력"):
        st.switch_page("pages/bidding_opening.py")

with col2:
    if st.button("📜 입찰정보 조회"):
        st.switch_page("pages/bidding_list.py")
    if st.button("🏆 개찰 결과 확인"):
        st.switch_page("pages/bidding_results.py")

st.markdown("---")

# ✅ 최근 등록된 입찰 섹션
st.markdown("### 📌 최근 등록된 입찰")
if recent_bids:
    for bid in recent_bids:
        st.markdown(f"📄 **{bid[0]}** (공고일: {bid[1]})")
else:
    st.markdown("📭 최근 등록된 입찰이 없습니다.")

st.markdown("---")

# ✅ 최근 개찰 완료된 입찰 섹션
st.markdown("### 🏆 최근 개찰 완료된 입찰")
if recent_openings:
    for opening in recent_openings:
        st.markdown(f"🏅 **{opening[0]}** → 낙찰업체: **{opening[1]}**")
else:
    st.markdown("📭 최근 개찰된 입찰이 없습니다.")

st.markdown("---")

# ✅ 푸터에 현재 연도 배치
st.markdown(f"© 2025 클레버디 | 입찰관리 시스템 v1.0 | 📅 현재 연도: **{current_year}년**")
