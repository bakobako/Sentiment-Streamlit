import streamlit as st
import pandas as pd

input_dir = '/data/in/tables/'


@st.cache_data
def read_df(file_name, index_col=None, date_col=None):
    return pd.read_csv(input_dir + file_name, index_col=index_col, parse_dates=date_col)


df = read_df('analyzed_output')

st.table(df)
