import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="\ud83c\udfe9\ufe0f \ud074\ub808\ubc84\ub514 \uc785\ucc29\uad00\ub9ac \uc2dc\uc2a4\ud15c", layout="wide")

# \ud504\ub85c\uc81d\ud2b8 \ubaa9\ub85d\uc744 \ubd88\ub7ec\uc624\ub294 \ud568\uc218
def get_data_file(year):
    return f"bidding_data_{year}.csv"

# \ubaa9\ub85d \uc870\ud68c\uc5d0 \uc0ac\uc6a9\ud560 \ud615\uc2dd \ubcc0
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
                if "\uc785\ucc29\uba85" in df.columns and "\uacf5\uace0\uc77c" in df.columns:
                    recent_bids.extend(df[["\uc785\ucc29\uba85", "\uacf5\uace0\uc77c"]].dropna().tail(3).values.tolist())
                if "\uc785\ucc29\uba85" in df.columns and "\ub0a9\ucc28\uc5c5\uccb4" in df.columns:
                    opened = df[df["\ub0a9\ucc28\uc5c5\uccb4"].str.strip() != ""]
                    recent_openings.extend(opened[["\uc785\ucc29\uba85", "\ub0a9\ucc28\uc5c5\uccb4"]].tail(3).values.tolist())

    return recent_bids, recent_openings

# \ubaa9\ub85d \ubd88\ub7ec\uc624\uae30
recent_bids, recent_openings = load_recent_data()
current_year = datetime.now().year

# \ub85c\uace0 \ud45c시
logo_path = "\ub85c\uace0.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=250)
else:
    st.image("https://via.placeholder.com/250x100?text=Clever:D", width=250)

st.markdown("<h1 style='text-align: center;'>\ud83c\udfe9\ufe0f \ud074\ub808\ubc84\ub514 \uc785\ucc29\uad00\ub9ac \uc2dc\uc2a4\ud15c</h1>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("## \ud83d\udcc2 \uba54\ub274")

if st.button("\ud83d\udcdd \uc785\ucc29\uc815\ubcf4 \uc785\ub825"):
    st.switch_page("pages/bidding_entry.py")
if st.button("\ud83d\udcca \uac1c\ucc28\uc815\ubcf4 \uc785\ub825"):
    st.switch_page("pages/bidding_opening.py")
if st.button("\ud83d\udcdc \uc785\ucc29\uc815\ubcf4 \uc870\ud68c"):
    st.switch_page("pages/bidding_list.py")
if st.button("\ud83c\udfc6 \uac1c\ucc28 \uacb0\uacfc \ud655\uc778"):
    st.switch_page("pages/bidding_results.py")

st.markdown("---")

# \ucc98\ub9ac\ub41c \ubaa9\ub85d \ud45c시
st.markdown("### \ud83d\udcc0 \ucd5c\uadfc \ub4f1\ub85d\ub41c \uc785\ucc29")
if recent_bids:
    for bid in recent_bids:
        bid_name, bid_date = bid[0], bid[1]
        if st.button(f"\ud83d\udcc4 {bid_name} (\uacf5\uace0\uc77c: {bid_date})", key=f"bid_{bid_name}"):
            st.experimental_set_query_params(bid=bid_name)
            st.switch_page("pages/bidding_list.py")
else:
    st.markdown("\ud83d\udcec \ucd5c\uadfc \ub4f1\ub85d\ub41c \uc785\ucc29\uc774 \uc5c6\uc2b5\ub2c8\ub2e4.")

st.markdown("---")

st.markdown("### \ud83c\udfc6 \ucd5c\uadfc \uac1c\ucc28 \uc644\ub8cc\ub41c \uc785\ucc29")
if recent_openings:
    for opening in recent_openings:
        opening_name, winner = opening[0], opening[1]
        if st.button(f"\ud83c\udfc5 {opening_name} \u2192 \ub0a9\ucc28\uc5c5\uccb4: {winner}", key=f"open_{opening_name}"):
            st.experimental_set_query_params(bid=opening_name)
            st.switch_page("pages/bidding_results.py")
else:
    st.markdown("\ud83d\udcec \ucd5c\uadfc \uac1c\ucc28\ub41c \uc785\ucc29\uc774 \uc5c6\uc2b5\ub2c8\ub2e4.")

st.markdown("---")
st.markdown(f"\u00a9 2025 \ud074\ub808\ubc84\ub514 | \uc785\ucc29\uad00\ub9ac \uc2dc\uc2a4\ud15c v1.0 | \ud83d\udcc5 \ud604\uc7ac \uc5f0\ub3c4: **{current_year}\ub144**")
