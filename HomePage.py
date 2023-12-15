import streamlit as st
from functions import *


appInfo()

st.title("Welcome to the home page")


with st.form(key='form1'):
    # text_input = st.text_input(label='Enter your search')
    # submit_button = st.form_submit_button(label='Search')
    submit_button = st.form_submit_button(label='Start Scraping Steam')



if submit_button:
    with st.spinner('Scraping in progress(may take 4-6 min)...'):
        try:
            df = steam_scrap()
            st.success('Scraping done!')
        except:
            st.error('Scraping failed!')
            st.stop()

    with st.spinner('Adding to database...'):
        try:
            dataToDB(df)
            st.success('Added to database!')
        except:
            st.error('Adding to database failed!')
            st.stop()

    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    st.download_button('Download CSV', df.to_csv() , f'games{date}.csv', 'text/csv')

    

