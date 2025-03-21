import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="📊 개찰정보 입력", layout="wide")

# ✅ 파일 경로 함수
def get_data_file(year):
    return f"bidding_data_{year}.csv"

# ✅ 파일 불러오기 함수
def load_data(year):
    file_name = get_data_file(year)
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame(columns=[
            "입찰공고번호", "입찰명", "공고일", "마감일", "사업기간", "사업예산", "과업내용", "입찰조건",
            "평가기준", "정량평가", "제출방법", "제출지역", "비고", "클레버디 투찰여부",
            "기술점수", "가격점수", "참여업체", "업체점수", "투찰금액", "낙찰업체", "담당자", "업체메모"
        ])

# ✅ 저장 함수
def save_data(df, year):
    file_name = get_data_file(year)
    df.to_csv(file_name, index=False)

st.title("📊 개찰정보 입력")

# ✅ 연도 자동 생성
current_year = datetime.now().year
year_options = [str(y) for y in range(current_year - 5, current_year + 4)]
default_year_index = year_options.index(str(current_year))
year = st.selectbox("연도 선택", year_options, index=default_year_index)

df = load_data(year)

# ✅ 데이터 존재 여부 확인
if df.empty or "입찰명" not in df.columns or df["입찰명"].isna().all():
    st.warning("📭 개찰할 입찰 정보가 없습니다. 먼저 입찰정보를 등록해주세요.")
    st.stop()

# ✅ 개찰할 입찰 선택
bid_titles = df["입찰명"].dropna().tolist()
selected_title = st.selectbox("개찰할 입찰 선택", bid_titles)

if not selected_title:
    st.warning("개찰할 입찰을 선택해주세요.")
    st.stop()

selected_index = df[df["입찰명"] == selected_title].index[0]

# ✅ 참여 업체 수
num_companies = st.number_input("참여 업체 수", min_value=1, step=1)

company_names = []
technical_scores = []
price_scores = []
notes = []
company_memos = []

for i in range(num_companies):
    st.markdown(f"#### 참여 업체 {i+1}")
    company_names.append(st.text_input(f"업체명 {i+1}", key=f"name_{i}"))
    technical_scores.append(st.number_input(f"기술점수 {i+1} (예: 78.1234)", key=f"tech_{i}", format="%.4f"))
    price_scores.append(st.number_input(f"가격점수 {i+1} (예: 19.8765)", key=f"price_{i}", format="%.4f"))
    notes.append(st.radio(f"비고 {i+1}", ["정상", "협상평가부적격"], key=f"note_{i}"))
    company_memos.append(st.text_input(f"업체 메모 {i+1}", key=f"memo_{i}"))

# ✅ 종합점수 계산
final_scores = [round(technical_scores[i] + price_scores[i], 4) for i in range(num_companies)]

# ✅ 순위 매기기
def get_ranks(scores):
    sorted_scores = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    ranks = [0] * len(scores)
    for rank, (idx, _) in enumerate(sorted_scores):
        ranks[idx] = rank + 1
    return ranks

ranks = get_ranks(final_scores)

# ✅ 저장 버튼
if st.button("저장"):
    try:
        winner = company_names[ranks.index(1)]

        df.at[selected_index, "참여업체"] = "; ".join(company_names)
        df.at[selected_index, "기술점수"] = "; ".join([str(x) for x in technical_scores])
        df.at[selected_index, "가격점수"] = "; ".join([str(x) for x in price_scores])
        df.at[selected_index, "업체점수"] = "; ".join([str(x) for x in final_scores])
        df.at[selected_index, "투찰금액"] = "-"  # 투찰금액 입력하지 않을 경우 기본값
        df.at[selected_index, "낙찰업체"] = winner
        df.at[selected_index, "업체메모"] = "; ".join(company_memos)

        save_data(df, year)
        st.success("✅ 개찰정보가 저장되었습니다!")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
