import streamlit as st
import pandas as pd
import os
from urllib.parse import unquote
from datetime import datetime

st.set_page_config(page_title="🏆 개찰정보 조회", layout="wide")
st.title("🏆 개찰정보 조회")

# ✅ URL에서 입찰명, 연도 가져오기
query_params = st.query_params
selected_bid = unquote(query_params.get("bid", [""])[0])
selected_year = query_params.get("year", [str(datetime.now().year)])[0]

# ✅ 데이터 파일 경로 함수
def get_data_file(year):
    return f"bidding_data_{year}.csv"

# ✅ 연도 확인 및 데이터 불러오기
try:
    years = [int(selected_year)]
except:
    years = [datetime.now().year - 1, datetime.now().year]

bidding_data = []
for year in years:
    file_path = get_data_file(year)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path).fillna("")
        bidding_data.append(df)

if bidding_data:
    df_all = pd.concat(bidding_data, ignore_index=True)
else:
    df_all = pd.DataFrame()

# ✅ 특정 입찰명으로 필터링
if selected_bid and not df_all.empty and "입찰명" in df_all.columns:
    df_filtered = df_all[df_all["입찰명"] == selected_bid]
    if not df_filtered.empty:
        bid_info = df_filtered.iloc[0]

        st.markdown(f"### 📌 개찰 정보 - {bid_info['입찰명']}")
        st.write(f"**📅 공고일:** {bid_info['공고일']} | **마감일:** {bid_info['마감일']}")
        st.write(f"**👤 담당자:** {bid_info.get('담당자', '미입력')}")
        st.write(f"**💰 사업 예산:** {int(bid_info['사업예산']):,} 만원")
        st.write(f"**📑 입찰 조건:** {bid_info.get('입찰조건', '미입력')}")

        st.markdown("---")
        st.markdown("### ✅ 개찰 결과")
        st.write(f"**🥇 낙찰 업체:** {bid_info['낙찰업체']}")
        st.write(f"**💸 투찰 금액:** {bid_info.get('투찰금액', '미입력')}")
        st.write(f"**📈 업체 점수:** {bid_info.get('업체점수', '미입력')}")
        st.write(f"**🧪 기술 점수:** {bid_info.get('기술점수', '미입력')} / **가격 점수:** {bid_info.get('가격점수', '미입력')}")
        st.write(f"**📊 평가 비율:** 기술 {bid_info.get('기술점수비율', '0')}점 / 가격 {bid_info.get('가격점수비율', '0')}점")

        if bid_info.get("정량평가", "").strip():
            st.write(f"**📋 정량평가:** {bid_info['정량평가']}")

        st.markdown("---")
        st.markdown("### 📎 기타 정보")
        st.write(f"**제출 방법:** {bid_info.get('제출방법', '미입력')} | 제출 지역: {bid_info.get('제출지역', '미입력')}")
        st.write(f"**클레버디 투찰 여부:** {bid_info.get('클레버디 투찰여부', '미입력')}")
        st.write(f"**비고:** {bid_info.get('비고', '없음')}")
    else:
        st.warning(f"⚠ '{selected_bid}'에 대한 개찰 정보가 없습니다.")
else:
    st.warning("📭 특정 개찰 정보를 조회하려면 목록에서 클릭하거나, URL에 파라미터를 포함시켜주세요.")
