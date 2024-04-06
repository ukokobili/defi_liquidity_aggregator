import pandas as pd
import psycopg2
import streamlit as st

# Database connection (replace with your actual connection details)
conn = psycopg2.connect(
    host='localhost', dbname='deFi', user='user', password='password'
)


# Querying transformed data
@st.cache
def get_data():
    query = "SELECT * FROM transformed_liquidity_data"
    return pd.read_sql(query, conn)


# Streamlit UI
def main():
    st.title('Liquidity Protocol Dashboard')

    df = get_data()
    protocol_names = df['protocol_name'].unique()

    selected_protocol = st.selectbox('Select a Protocol', protocol_names)
    filtered_df = df[df['protocol_name'] == selected_protocol]

    st.write('Data for selected protocol:')
    st.write(filtered_df)


if __name__ == "__main__":
    main()
