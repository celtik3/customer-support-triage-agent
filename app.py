import streamlit as st

st.set_page_config(page_title="Customer Support Triage Agent", layout="wide")

st.title("Multi-Agent Customer Support Triage System")
st.write("Hour 1 setup test: Streamlit is running successfully.")

user_request = st.text_area("Paste a customer support request:")

if st.button("Run Triage"):
    st.write("Input received:")
    st.write(user_request)