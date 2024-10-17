import streamlit as st
from datetime import datetime

from utils import save_to_excel, show_download_link
from fetcher import fetch_dart_data, fetch_company_data, fetch_report_data


def display_by_category(api_key):
    st.header("분류별 데이터 추출")
    kind_detail = st.text_input("분류(Kind Detail) 코드를 입력하세요 (예: D003)", value="D003")
    year = st.number_input("수집할 분류의 연도를 입력하세요", min_value=1900, max_value=datetime.now().year, value=datetime.now().year)
    
    if st.button("분류 데이터 수집 시작"):
        if not api_key:
            st.error("API 키를 입력해주세요.")
            return

        st.write(f"{year}년 데이터 수집을 시작합니다...")

        try:
            data = fetch_dart_data(api_key, kind_detail, year)

            if data.empty:
                st.error("수집된 데이터가 없습니다.")
            else:
                st.success("데이터 수집이 완료되었습니다.")
                st.dataframe(data)

                # Create a download button for the Excel file
                buffer = save_to_excel(data)
                filename = f'DART_{year}_{kind_detail}.xlsx'
                show_download_link(buffer, filename)
        except Exception as e:
            st.error(f"데이터 수집 중 오류가 발생했습니다: {str(e)}")

def display_by_company(api_key):
    st.header("회사 정기 보고서 추출")
    company_code = st.text_input("종목 코드를 입력하세요 (예: 010130)", value="010130")
    year = st.number_input("수집할 회사의 연도를 입력하세요", min_value=1900, max_value=datetime.now().year, value=datetime.now().year)

    if st.button("회사 데이터 수집 시작"):
        if not api_key:
            st.error("API 키를 입력해주세요.")
            return

        try:
            company_data = fetch_company_data(api_key, company_code, year)
            if company_data.empty:
                st.error("수집된 회사 데이터가 없습니다.")

            rcept_no_list = company_data['rcept_no'].tolist()
            for rcept_no in rcept_no_list:
                fetch_report_data(api_key, rcept_no)
            st.success("회사 데이터 수집이 완료되었습니다.")
        except Exception as e:
            st.error(f"회사 데이터 수집 중 오류가 발생했습니다: {str(e)}")


def main():
    st.title("DART 데이터 수집기")
    api_key = st.text_input("DART API 키를 입력하세요", type="password")

    display_by_category(api_key)
    st.write("---")  # Separator between sections
    display_by_company(api_key)

if __name__ == "__main__":
    main()