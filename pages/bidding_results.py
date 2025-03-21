import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="📈 개찰 정보 조회", layout="wide")

def get_data_file(year):
    return f"bidding_data_{year}.csv"

def load_data(year):
    file_name = get_data_file(year)
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame()

st.title("📈 개찰 정보 조회")

# ✅ 연도 선택 (자동)
current_year = datetime.now().year
year_options = [str(y) for y in range(current_year - 5, current_year + 4)]
default_year = st.session_state.get("선택연도", str(current_year))
default_year_index = year_options.index(default_year) if default_year in year_options else 0

year = st.selectbox("연도 선택", year_options, index=default_year_index)
df = load_data(year)

if df.empty:
    st.warning("⚠ 등록된 입찰 정보가 없습니다.")
else:
    # ✅ 개찰 완료된 입찰만 필터링
    opened_df = df[df["낙찰업체"].notna() & (df["낙찰업체"].str.strip() != "")]

    if opened_df.empty:
        st.info("ℹ 개찰이 완료된 입찰이 없습니다.")
    else:
        bid_list = opened_df["입찰명"].tolist()
        default_selection = st.session_state.get("선택입찰명", bid_list[0])
        if default_selection in bid_list:
            selected_title = st.selectbox("조회할 입찰명 선택", bid_list, index=bid_list.index(default_selection))
        else:
            selected_title = st.selectbox("조회할 입찰명 선택", bid_list)

        bid_data = opened_df[opened_df["입찰명"] == selected_title].iloc[0]

        st.markdown(f"## 📌 입찰명: {bid_data['입찰명']}")
        st.write(f"- 입찰공고번호: {bid_data['입찰공고번호']}")
        st.write(f"- 공고일: {bid_data['공고일']} / 마감일: {bid_data['마감일']}")
        st.write(f"- 낙찰업체: 🏆 {bid_data['낙찰업체']}")
        st.write(f"- 담당자: {bid_data['담당자']}")

        st.markdown("### 📋 참여 업체별 개찰 정보")

        # ✅ 안전하게 split 처리 (빈 값 대비)
        def safe_split(value):
            return [v.strip() for v in str(value).split(";")] if pd.notna(value) and str(value).strip() else []

        companies = safe_split(bid_data.get("참여업체", ""))
        tech_scores = safe_split(bid_data.get("기술점수", ""))
        price_scores = safe_split(bid_data.get("가격점수", ""))
        total_scores = safe_split(bid_data.get("업체점수", ""))
        company_memos = safe_split(bid_data.get("업체메모", ""))

        # ✅ 종합점수 float 변환 및 순위 계산
        try:
            float_scores = [float(s) for s in total_scores]
            sorted_scores = sorted(enumerate(float_scores), key=lambda x: x[1], reverse=True)
            ranks = [0] * len(float_scores)
            for rank, (idx, _) in enumerate(sorted_scores):
                ranks[idx] = rank + 1
        except:
            ranks = ["-"] * len(companies)

        # ✅ 표 데이터 구성
        result_data = []
        for i in range(len(companies)):
            result_data.append({
                "업체명": companies[i] if i < len(companies) else "",
                "기술점수": tech_scores[i] if i < len(tech_scores) else "",
                "가격점수": price_scores[i] if i < len(price_scores) else "",
                "종합점수": total_scores[i] if i < len(total_scores) else "",
                "순위": ranks[i] if i < len(ranks) else "",
                "업체메모": company_memos[i] if i < len(company_memos) else ""
            })

        if result_data:
            result_df = pd.DataFrame(result_data)
            st.dataframe(result_df, use_container_width=True)
        else:
            st.warning("📭 등록된 개찰 상세 정보가 없습니다.")
