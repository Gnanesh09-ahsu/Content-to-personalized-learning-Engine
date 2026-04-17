import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
import requests
import time
from streamlit_lottie import st_lottie

st.set_page_config(page_title="AI Learning Engine", layout="wide")


def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_study = load_lottie("https://assets10.lottiefiles.com/packages/lf20_kyu7xb1v.json")
lottie_success = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jbrw3hcz.json")

st.title("AI Personalized Learning Engine")
st.caption("AI-powered adaptive learning system for smarter studying")

st_lottie(lottie_study, height=200)

if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "score" not in st.session_state:
    st.session_state.score = None
if "level" not in st.session_state:
    st.session_state.level = "medium"
if "history" not in st.session_state:
    st.session_state.history = []

content = st.text_area("Paste your notes:", height=200)

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    pdf = PyPDF2.PdfReader(uploaded_file)
    text = "".join([page.extract_text() or "" for page in pdf.pages])
    content = text
    st.success("PDF content loaded!")

def generate_questions(text, level):
    text = text.lower()

    questions = [
        "What is the main idea of the topic?",
        "Explain the concept in your own words.",
        "Why is this topic important?",
    ]

    if "process" in text:
        questions.append("Describe the steps involved in this process.")

    if level == "easy":
        questions.append("Give a simple example.")
    elif level == "hard":
        questions.extend([
            "What are limitations of this concept?",
            "Apply this in real life."
        ])

    questions.append("Explain this like I'm 5 years old.")

    return questions

if st.button("Generate Questions"):
    if content.strip() == "":
        st.warning("Please enter or upload content!")
    else:
        with st.spinner("Generating questions..."):
            time.sleep(1.5)
            st.session_state.questions = generate_questions(content, st.session_state.level)
            st.session_state.answers = {}
            st.session_state.score = None

if st.session_state.questions:
    st.subheader(f"Questions (Level: {st.session_state.level.upper()})")

    for i, q in enumerate(st.session_state.questions):
        ans = st.text_area(f"{q}", key=f"q_{i}")
        st.session_state.answers[i] = ans

    if st.button("Submit Answers"):
        score = 0
        for ans in st.session_state.answers.values():
            if ans and len(ans) > 15:
                score += 1

        st.session_state.score = score
        st.session_state.history.append(score)

if st.session_state.score is not None:
    total = len(st.session_state.questions)
    st.success(f"Score: {st.session_state.score} / {total}")

    st_lottie(lottie_success, height=150)

    if st.session_state.score <= 2:
        st.session_state.level = "easy"
        st.warning("Switching to EASY level")
    elif st.session_state.score == total:
        st.session_state.level = "hard"
        st.info("Switching to HARD level")
    else:
        st.session_state.level = "medium"
        st.info("Staying at MEDIUM level")

    if st.button("Next Round"):
        st.session_state.questions = generate_questions(content, st.session_state.level)
        st.session_state.answers = {}
        st.session_state.score = None

st.markdown("---")
st.subheader("Your Progress")

if st.session_state.history:
    fig, ax = plt.subplots()
    ax.plot(st.session_state.history, marker='o')
    ax.set_title("Learning Progress")
    ax.set_xlabel("Attempt")
    ax.set_ylabel("Score")
    st.pyplot(fig)
else:
    st.write("No progress yet.")

st.markdown("---")

if st.button("Explain Like I'm 5yr old kid"):
    if content:
        text = content.lower()

        if "photosynthesis" in text:
            explanation = "Plants use sunlight to make food and give us oxygen."
        elif "machine learning" in text:
            explanation = "A computer learns from examples and gets better."
        else:
            explanation = "This is a simple idea about how something works."

        st.success(explanation)

st.markdown("---")
