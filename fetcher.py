import base64
import pandas as pd
import OpenDartReader
import streamlit as st

from utils import get_quarterly_dates

# 해당 종목의 공시 리스트 수집
@st.cache_data
def fetch_dart_data(api_key, kind_detail, year):
    dart = OpenDartReader(api_key)
    all_data = []
    quarters = get_quarterly_dates(year)

    for start_date, end_date in quarters:
        st.write(f"데이터 수집 중: {start_date} to {end_date}")
        data = dart.list(start=start_date, end=end_date, kind_detail=kind_detail)
        all_data.append(data)

    return pd.concat(all_data, ignore_index=True)

# 회사의 정기보고서 리스트 수집
@st.cache_data
def fetch_company_data(api_key, company_code, year):
    dart = OpenDartReader(api_key)
    all_data = []
    quarters = get_quarterly_dates(year)

    for start_date, end_date in quarters:
        st.write(f"데이터 수집 중: {start_date} to {end_date}")
        data = dart.list(company_code, start=start_date, end=end_date, kind='A')
        all_data.append(data)

    return pd.concat(all_data, ignore_index=True)


# 개별 보고서 내용 수집
@st.cache_data
def fetch_report_data(api_key, rcept_no):
    dart = OpenDartReader(api_key)
    xml_text = dart.document(rcept_no)
    file_name = f"{rcept_no}.xml"

    # Create a download link
    b64 = base64.b64encode(xml_text.encode()).decode()  # Convert to base64
    href = f'<a href="data:text/xml;base64,{b64}" download="{file_name}">Download XML for rcept_no: {rcept_no}</a>'
    st.markdown(href, unsafe_allow_html=True)