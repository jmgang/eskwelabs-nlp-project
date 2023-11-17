
import streamlit as st
from streamlit_chat import message
from core import retrieve_job_information, retrieve_job_ids

st.title("NLP Sprint Project")
st.caption("by: Eswelabs The Explorers")
st.image("https://www.creativefabrica.com/wp-content/uploads/2020/05/16/Write-a-resume-and-cv-to-apply-for-job-Graphics-4132681-1.jpg")
st.divider()

prompt = st.text_input("Talk with our Job specialist who specializes in engineering positions in the data science "
					   "and product development space",
					   placeholder="Enter your skills here...") or st.button(
	"Submit"
)

if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

if prompt:
	with st.spinner("Generating response..."):
		response = retrieve_job_information(retrieve_job_ids(prompt))
		st.session_state.chat_history.append((prompt, response))
		st.session_state.user_prompt_history.append(prompt)
		st.session_state.chat_answers_history.append(response)


message(
	"Hi! I am JobExplorerGPT. I am a job helper that specializes in engineering positions in data science and product development. "
	"Let me know what skills or job description you are envisioning and I'll help you find suitable jobs with its responsibilities "
	"and required skills. ")

if st.session_state["chat_answers_history"]:
	for generated_response, user_query in zip(
			st.session_state["chat_answers_history"],
			st.session_state["user_prompt_history"],
	):
		message(
			user_query, is_user=True
		)
		message(generated_response)