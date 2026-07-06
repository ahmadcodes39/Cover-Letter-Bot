import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

st.set_page_config(page_title="Cover Letter Bot", page_icon="✉️")

st.title("✉️ Cover Letter & Cold Email Tailor Bot")
st.write("Paste a job description and I'll help you draft a tailored cover letter or cold email.")

job_description = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder="e.g. We are looking for a Full Stack Developer with experience in React, Node.js..."
)

your_background = st.text_area(
    "Paste your CV summary / key skills here",
    height=150,
    placeholder="e.g. BSCS graduate, MERN stack, worked on RAG pipelines, internship at..."
)

output_type = st.radio(
    "What do you want to generate?",
    ["Cold Email", "Cover Letter"],
    horizontal=True
)

generate_clicked = st.button("Generate")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def generate_content(job_desc, background, out_type):
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""You are an expert career assistant helping a job seeker write a tailored {out_type}.

Job Description:
{job_desc}

Candidate Background:
{background}

Write a professional, concise {out_type} tailored specifically to this job description, highlighting the most relevant parts of the candidate's background. Keep it natural, not generic."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e).lower()
        if "quota" in error_msg or "rate" in error_msg:
            return "⚠️ Rate limit or quota reached. Please wait a moment and try again."
        elif "safety" in error_msg:
            return "⚠️ The content was blocked by safety filters. Try rephrasing the job description or background."
        else:
            return f"⚠️ Something went wrong: {str(e)}"
        
        
if generate_clicked:
    if not job_description or not your_background:
        st.warning("Please fill in both the job description and your background.")
    elif len(job_description) > 8000 or len(your_background) > 4000:
        st.warning("Input is too long. Please shorten the job description or background.")
    else:
        with st.spinner("Generating..."):
            result = generate_content(job_description, your_background, output_type)
        st.session_state.chat_history = [
            {"role": "user", "content": f"Generate a {output_type} for this job."},
            {"role": "assistant", "content": result}
        ]
        
# Show the conversation so far
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Follow-up input box, only show if there's already a generated draft
if st.session_state.chat_history:
    follow_up = st.chat_input("Ask for changes, e.g. 'make it shorter' or 'more formal tone'")
    if follow_up:
        st.session_state.chat_history.append({"role": "user", "content": follow_up})
        
        model = genai.GenerativeModel("gemini-2.5-flash")
        convo_text = ""
        for msg in st.session_state.chat_history:
            convo_text += f"{msg['role']}: {msg['content']}\n\n"
        
        try:
            with st.spinner("Updating..."):
                response = model.generate_content(convo_text)
            reply = response.text
        except Exception as e:
            reply = f"⚠️ Something went wrong: {str(e)}"
        
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()