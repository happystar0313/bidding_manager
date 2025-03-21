import streamlit as st
import pandas as pd
import os
from datetime import datetime
from urllib.parse import unquote, quote
import streamlit.components.v1 as components

st.set_page_config(page_title="📜 입찰정보 리스트", layout="wide")

def get_data_file(year):
    return f"bidding_data_{year}.csv"

def load_data(year):
    file_name = get_data_file(year)
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame(columns=[
            "입찰공고번호", "입찰명", "공고일", "마감일", "사업기간", "사업예산", "과업내용", "입찰조건",
            "기술점수비율", "가격점수비율", "정량평가", "기술점수", "가격점수", "참여업체", "업체점수", "투찰금액", 
            "낙찰업체", "담당자", "제출방법", "제출지역", "비고", "클레버디 투찰여부"
        ])

st.title("📜 입찰정보 리스트")

# ✅ 연도 선택 자동화
current_year = datetime.now().year
year_options = [str(y) for y in range(current_year - 5, current_year + 4)]
def_year_idx = year_options.index(str(current_year))
year = st.selectbox("연도 선택", year_options, index=def_year_idx)

df = load_data(year)
df["개찰여부"] = df["낙찰업체"].apply(lambda x: "⭕ 개찰 완료" if pd.notna(x) and x.strip() != "" else "❌ 미개찰")

# ✅ URL에서 전달된 입찰명 자동 선택
query_params = st.query_params
selected_bid = query_params.get("bid", [""])[0]
selected_bid = unquote(selected_bid)

if not df.empty:
    st.write("### 📋 입찰 목록")
    selected_bid = st.selectbox("상세 조회할 입찰 선택", df["입찰명"].tolist(), 
                                index=df["입찰명"].tolist().index(selected_bid) if selected_bid in df["입찰명"].tolist() else 0)

    bid_data = df[df["입찰명"] == selected_bid].iloc[0]

    st.write(f"### 📌 입찰명: {bid_data['입찰명']}")
    st.write(f"👤 담당자: {bid_data.get('담당자', '미입력')}")
    st.write(f"📅 공고일: {bid_data['공고일']} | 마감일: {bid_data['마감일']}")
    st.write(f"💰 사업예산: {int(bid_data['사업예산']) * 10_000:,} 원")
    st.write(f"📌 개찰 상태: {bid_data['개찰여부']}")
    st.write(f"📏 정량평가 기준: {bid_data.get('정량평가기준', '미입력')}")
    st.write(f"📤 제출 방법: {bid_data.get('제출방법', '미입력')}")
    st.write(f"📌 클레버디 투찰 여부: {bid_data.get('클레버디 투찰여부', '미입력')}")
    st.write(f"📝 비고: {bid_data.get('비고', '없음')}")

    tech_ratio = bid_data.get("기술점수비율", "")
    price_ratio = bid_data.get("가격점수비율", "")
    st.write(f"📊 평가 기준: **기술 {tech_ratio}점 / 가격 {price_ratio}점**")

    if isinstance(bid_data.get("정량평가", ""), str) and bid_data["정량평가"].strip():
        st.write(f"📋 **정량평가 항목**: {bid_data['정량평가']}")

    # ✅ 개찰 완료 시 안전한 JS 방식으로 이동
    if bid_data["개찰여부"] == "⭕ 개찰 완료":
        st.success("🏆 개찰이 완료된 입찰입니다.")
        if st.button("📊 개찰 정보 조회"):
            encoded_bid = quote(bid_data["입찰명"])
            target_url = f"./bidding_results.py?bid={encoded_bid}&year={year}"
            components.html(f"""<script>window.location.href = '{target_url}';</script>""", height=0)
    else:
        st.warning("⚠ 이 입찰은 아직 개찰되지 않았습니다.")
else:
    st.warning("⚠ 등록된 입찰 정보가 없습니다.")
