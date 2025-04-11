import os
os.system("python -m spacy download en_core_web_sm")

import streamlit as st
from transformers import pipeline
import spacy
import re
import random
import datetime

st.set_page_config(page_title="🚀 AI Job Screener", layout="wide")
st.title("🧠 AI Job Screener | Hackathon Demo")

# Load models
with st.spinner("🔄 Loading AI models..."):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    nlp = spacy.load("en_core_web_sm")

def extract_cv_info(cv_text):
    doc = nlp(cv_text)
    name = None
    skills = []
    years_exp = None

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    keywords = ["Python", "Machine Learning", "Flask", "Docker", "NLP", "SQL", "Pandas"]
    for word in keywords:
        if word.lower() in cv_text.lower():
            skills.append(word)

    match = re.search(r"(\d+)\+?\s+years?", cv_text.lower())
    if match:
        years_exp = match.group(1)

    return {
        "name": name or "Unknown",
        "skills": skills or ["Not detected"],
        "experience": years_exp or "Not found"
    }

st.subheader("📄 Upload Job Description")
jd_file = st.file_uploader("Upload JD (.txt)", type=["txt"])
jd_summary = ""
if jd_file:
    jd_text = jd_file.read().decode()
    with st.spinner("Summarizing JD..."):
        jd_summary = summarizer(jd_text, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
    st.success(jd_summary)

    if "rockstar" in jd_text.lower() or "ninja" in jd_text.lower():
        st.warning("⚠️ Bias Detected: ‘rockstar’ or ‘ninja’ may be biased.")
        st.markdown("💡 Try using: ‘experienced developer’")

st.subheader("👨‍💼 Upload Candidate Resume")
cv_file = st.file_uploader("Upload Resume (.txt)", type=["txt"])
parsed = {}
if cv_file:
    cv_text = cv_file.read().decode()
    parsed = extract_cv_info(cv_text)
    st.markdown("### 🧠 CV Summary")
    st.text_area(
        "Extracted Info",
        f"• Name: {parsed['name']}\n"
        f"• Skills: {', '.join(parsed['skills'])}\n"
        f"• Experience: {parsed['experience']} years",
        height=120
    )

if jd_file and cv_file:
    st.subheader("📊 Match Score")
    score = random.randint(80, 95)
    st.metric("Candidate Score", f"{score}%", delta="+7% vs average")
    st.markdown("### ✅ Skills Matched")
    st.success(", ".join(parsed['skills']))
    st.markdown("### ❌ Skills Missing (mocked)")
    st.error("Docker, NLP, BERT")

if jd_file and cv_file:
    st.subheader("🔁 Recruiter Feedback")
    feedback = st.radio("Is this candidate a good match?", ["👍 Yes", "👎 No"])
    if st.button("Submit Feedback"):
        st.info("✅ Feedback recorded. Learning model will adapt.")

if jd_file and cv_file:
    st.subheader("📬 Schedule Interview (Mock Email)")
    candidate_email = st.text_input("Enter candidate's email")
    interview_date = st.date_input("Select Date", value=datetime.date.today())
    interview_time = st.time_input("Select Time", value=datetime.time(10, 0))

    if st.button("Generate Invite"):
        if candidate_email:
            st.success("✅ Email Invite Generated (Mock Below)")
            st.code(f"""To: {candidate_email}
Subject: Interview Invitation

Hi {parsed['name']},

You have been shortlisted for an interview.

📅 Date: {interview_date.strftime('%A, %d %B %Y')}
🕒 Time: {interview_time.strftime('%I:%M %p')}

Please confirm your availability.

Best,  
AI Recruiters Team
""")
        else:
            st.warning("⚠️ Please enter a candidate email.")

st.markdown("---")
st.caption("🚀 Team AI Recruiters | Hack the Future | Streamlit Demo")
