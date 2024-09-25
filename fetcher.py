import streamlit as st
import OpenDartReader
import pandas as pd
from datetime import datetime
import io

def get_quarterly_dates(year):
    return [
        (f"{year}-01-01", f"{year}-03-31"),
        (f"{year}-04-01", f"{year}-06-30"),
        (f"{year}-07-01", f"{year}-09-30"),
        (f"{year}-10-01", f"{year}-12-31")
    ]

@st.cache_data
def fetch_dart_data(year, api_key, kind_detail):
    dart = OpenDartReader(api_key)

    all_data = []
    quarters = get_quarterly_dates(year)

    for start_date, end_date in quarters:
        st.write(f"데이터 수집 중: {start_date} to {end_date}")
        data = dart.list(start=start_date, end=end_date, kind_detail=kind_detail)
        all_data.append(data)

    return pd.concat(all_data, ignore_index=True)

def main():
    st.title("DART 데이터 수집기")

    # User inputs
    api_key = st.text_input("DART API 키를 입력하세요", type="password")
    kind_detail = st.text_input("Kind Detail 코드를 입력하세요 (예: D003)", value="D003")
    year = st.number_input("데이터를 수집할 연도를 입력하세요", min_value=1900, max_value=datetime.now().year, value=datetime.now().year)

    if st.button("데이터 수집 시작"):
        if not api_key:
            st.error("API 키를 입력해주세요.")
            return

        st.write(f"{year}년 데이터 수집을 시작합니다...")

        try:
            data = fetch_dart_data(year, api_key, kind_detail)

            if data.empty:
                st.error("수집된 데이터가 없습니다.")
            else:
                st.success("데이터 수집이 완료되었습니다.")
                st.dataframe(data)  # Display the data in the Streamlit app

                # Create a download button for the Excel file
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    data.to_excel(writer, index=False, sheet_name='Sheet1')
                buffer.seek(0)

                filename = f'DART_데이터_{year}_{kind_detail}.xlsx'
                st.download_button(
                    label="Excel 파일 다운로드",
                    data=buffer,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"데이터 수집 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()