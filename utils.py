import io
import pandas as pd
import streamlit as st


def get_quarterly_dates(year):
    return [
        (f"{year}-01-01", f"{year}-03-31"),
        (f"{year}-04-01", f"{year}-06-30"),
        (f"{year}-07-01", f"{year}-09-30"),
        (f"{year}-10-01", f"{year}-12-31")
    ]

def save_to_excel(data, sheet_name='Sheet1', multi_sheet=False):
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        if multi_sheet:
            for key, df in data.items():
                df.to_excel(writer, index=False, sheet_name=key)
        else:
            data.to_excel(writer, index=False, sheet_name=sheet_name)
    
    buffer.seek(0)
    return buffer


def show_download_link(buffer, filename):
    st.download_button(
        label="Excel 파일 다운로드",
        data=buffer,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )