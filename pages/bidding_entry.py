import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="📢 입찰정보 입력", layout="wide")

def get_data_file(year):
    return f"bidding_data_{year}.csv"

def load_data(year):
    file_name = get_data_file(year)
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame()

st.title("📢 신규 입찰정보 입력")

# ✅ 연도 선택 (과거 5년 ~ 미래 3년 자동 생성)
current_year = datetime.now().year
year_options = [str(y) for y in range(current_year - 5, current_year + 4)]
default_year_index = year_options.index(str(current_year))
year = st.selectbox("입찰 연도 선택", year_options, index=default_year_index)

df = load_data(year)

# ✅ 입력 필드들
title = st.text_input("입찰명")
number = st.text_input("입찰공고번호")
open_date = st.date_input("공고일")
deadline = st.date_input("마감일")
budget = st.number_input("사업예산 (단위: 만원)", min_value=0, step=100)
manager = st.text_input("담당자 (입찰 담당자)")
cleverbid_status = st.selectbox("클레버디 투찰여부", ["예", "아니오", "보류"])

# ✅ 등록 버튼
if st.button("입찰정보 등록"):
    new_data = pd.DataFrame([{
        "입찰공고번호": number,
        "입찰명": title,
        "공고일": open_date,
        "마감일": deadline,
        "사업예산": budget,
        "담당자": manager,
        "클레버디 투찰여부": cleverbid_status
    }])

    updated_df = pd.concat([df, new_data], ignore_index=True)
    updated_df.to_csv(get_data_file(year), index=False)
    st.success("입찰정보가 성공적으로 등록되었습니다!")