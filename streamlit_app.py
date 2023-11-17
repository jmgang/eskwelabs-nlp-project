import pandas as pd
import streamlit as st

st.title("NLP Sprint Project")
st.caption("by: Eswelabs The Explorers")
st.image("https://www.creativefabrica.com/wp-content/uploads/2020/05/16/Write-a-resume-and-cv-to-apply-for-job-Graphics-4132681-1.jpg")
st.divider()

st.text_input("Enter your input here")

def function():
	return ""

if st.button("Submit", type="primary"):
	function()