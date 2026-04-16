import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Learning Engine", layout="wide")

st.title("AI Personalized Learning Engine")
st.write("Upload notes or PDFs → Get quizzes → Improve with adaptive learning")

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

    base_questions = [
        "What is the main idea of the topic?",
        "Explain the concept in your own words.",
        "Why is this topic important?",
    ]

    if "process" in text or "steps" in text:
        base_questions.append("Describe the steps involved in this process.")

    if "define" in text or "is" in text:
        base_questions.append("Define the key term mentioned.")

    if level == "easy":
        base_questions.append("Give a simple example of this concept.")

    elif level == "hard":
        base_questions.extend([
            "What are the limitations of this concept?",
            "Apply this concept to a real-world scenario."
        ])

    base_questions.append("Explain this topic like I'm 5 years old.")

    return base_questions

if st.button("Generate Questions"):
    if content.strip() == "":
        st.warning("Please enter or upload content!")
    else:
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

    if st.session_state.score <= 2:
        st.session_state.level = "easy"
        st.warning("Weak → Switching to EASY level")
    elif st.session_state.score == total:
        st.session_state.level = "hard"
        st.info("Strong → Switching to HARD level")
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

if st.button("Explain Like I'm 5 yr old kid"):
    if content:
        st.info("This topic in simple words:\n\n" + content[:200] + "...")

st.markdown("---")
