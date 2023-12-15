import streamlit as st
import pandas as pd
from functions import *

appInfo()

st.title("Historique")


try:
    database = DataBase('games')

    tables = database.get_tables()

    selectTable =  st.selectbox('Select a table', tables)

    table = database.select_table(selectTable)

    df = pd.DataFrame(table)

    if df.empty:
        st.info('No data to display', icon='🤖')
    else:
        st.write(df)

except:
    st.error('No database found, please scrap steam first', icon='🤖')