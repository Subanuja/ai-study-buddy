import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from backboard import BackboardClient

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fc;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    .hero {
        background: linear-gradient(135deg, #4338ca, #7c3aed);
        padding: 35px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 38px;
        margin-bottom: 10px;
    }

    .hero p {
        color: #ede9fe;
        font-size: 17px;
    }

    .feature-card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        min-height: 155px;
        margin-bottom: 12px;
    }

    .feature-card h3 {
        color: #312e81;
        margin-top: 5px;
    }

    .feature-card p {
        color: #64748b;
    }

    .section-title {
        color: #1e293b;
        font-size: 25px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        min-height: 45px;
    }

    div.stButton > button:hover {
        background: #3730a3;
        color: white;
        border: none;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        border-radius: 10px;
    }

    .result-box {
        background: white;
        padding: 24px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown("# 📚 Study Buddy")
    st.caption("YOUR PERSONAL AI LEARNING PARTNER")

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "📖 AI Study Tools",
            "💬 AI Study Chat",
            "ℹ️ About Project"
        ],
        label_visibility="visible"
    )

    st.markdown("---")
    st.caption("🎓 Built for students")
    st.caption("💜 Learn smarter, not harder.")


# AI API configuration
api_key = os.getenv("BACKBOARD_API_KEY")


# Function to communicate with Backboard
async def get_ai_response(prompt):
    async with BackboardClient(api_key=api_key) as client:
        response = await client.send_message(
            prompt,
            stream=False
        )
        return response.content


def generate_answer(prompt):
    try:
        return asyncio.run(get_ai_response(prompt))
    except Exception as error:
        st.error(
            "Sorry, the AI request could not be completed. "
            "Please check your API key, internet connection, "
            "and Backboard account."
        )
        st.caption(f"Technical details: {error}")
        return None


# Dashboard page
if page == "🏠 Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Welcome to AI Study Buddy 👋</h1>
        <p>Your smart learning companion for university life.</p>
        <p>Understand topics, create notes, and practise with quizzes.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Your AI Learning Tools</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📘 Topic Explainer</h3>
            <p>Understand difficult ICT concepts with simple explanations.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 Study Notes</h3>
            <p>Generate organised notes for your university studies.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 Quiz Generator</h3>
            <p>Practise your knowledge with AI-generated questions.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">How can I help you today?</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Choose **AI Study Tools** from the sidebar to get started."
    )

    st.info(
        "💡 Tip: Start with a topic you are currently learning "
        "at university."
    )


# AI Study Tools page
elif page == "📖 AI Study Tools":

    st.markdown("""
<div class="hero">
    <h1>📖 AI Study Workspace</h1>
    <p>Choose your tool below and start learning.</p>
</div>
""", unsafe_allow_html=True)

    if not api_key:
        st.error(
            "API key not found. Please check your .env file."
        )
        st.stop()

    task = st.selectbox(
        "Choose a study tool",
        [
            "📘 Explain a Topic",
            "📝 Generate Study Notes",
            "🧠 Generate Quiz Questions"
        ]
    )

    topic = st.text_input(
        "Enter your ICT topic",
        placeholder="Example: Java Variables"
    )

    level = st.selectbox(
        "Your learning level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    if task == "📘 Explain a Topic":
        st.caption(
            "Get a simple explanation with examples and key concepts."
        )

    elif task == "📝 Generate Study Notes":
        st.caption(
            "Create organised revision notes with headings and examples."
        )

    else:
        st.caption(
            "Generate five practice questions with an answer key."
        )

    if st.button("✨ Generate", use_container_width=True):

        if not topic.strip():
            st.warning("Please enter a topic first.")

        else:

            if task == "📘 Explain a Topic":
                prompt = (
                    f"Explain {topic} to an ICT university student "
                    f"at {level} level. Use simple English, "
                    "step-by-step explanations, examples, "
                    "and important key points."
                )

            elif task == "📝 Generate Study Notes":
                prompt = (
                    f"Create clear study notes about {topic} "
                    f"for a {level} student. Use headings, "
                    "definitions, bullet points, important concepts, "
                    "and examples. Format the answer in Markdown."
                )

            else:
                prompt = (
                    f"Create 5 quiz questions about {topic} "
                    f"for a {level} student. Provide multiple-choice "
                    "options, then give the correct answers and "
                    "brief explanations in a separate answer key."
                )

            with st.spinner("Your AI study assistant is working..."):
                answer = generate_answer(prompt)

            if answer:
                st.markdown("---")
                st.subheader("📚 Your Study Result")
                st.markdown(answer)

                st.download_button(
                    label="⬇️ Download Result",
                    data=answer,
                    file_name="ai_study_result.md",
                    mime="text/markdown"
                )
# AI Study Chat page
elif page == "💬 AI Study Chat":

    st.markdown("""
    <div class="hero">
        <h1>AI Study Chat 💬</h1>
        <p>Ask questions, understand concepts, and learn step by step.</p>
    </div>
    """, unsafe_allow_html=True)

    if not api_key:
        st.error("API key not found. Please check your .env file.")
        st.stop()

    # Initialise conversation history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Clear chat button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.chat_messages = []
        st.rerun()

    # Display previous messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_prompt = st.chat_input(
        "Ask anything about your studies..."
    )

    if user_prompt:

        # Save and display user's message
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_prompt
        })

        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Include previous conversation for context
        conversation_history = ""

        for message in st.session_state.chat_messages[-12:]:
            if message["role"] == "user":
                conversation_history += (
                    f"\nStudent: {message['content']}\n"
                )
            else:
                conversation_history += (
                    f"\nAI Study Buddy: {message['content']}\n"
                )

        full_prompt = f"""
You are AI Study Buddy, a friendly AI learning assistant
for university students.

Your job:
- Explain difficult concepts in simple English.
- Give step-by-step explanations for beginners.
- Provide examples, especially for ICT and programming.
- Answer follow-up questions using the conversation context.
- If a student asks for code, explain the code clearly.

Previous conversation:
{conversation_history}

Respond helpfully to the student's latest message.
"""

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("AI Study Buddy is thinking..."):
                answer = generate_answer(full_prompt)

            if answer:
                st.markdown(answer)

                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer
                })

# About page
elif page == "ℹ️ About Project":

    st.markdown("""
    <div class="hero">
        <h1>About AI Study Buddy 💜</h1>
        <p>Your personal space to learn, practise, and improve.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎯 What can AI Study Buddy do?")

    st.write(
        "AI Study Buddy helps you learn university topics in simple language. "
        "You can create study notes, practise with quiz questions, and ask "
        "follow-up questions in the AI Study Chat."
    )

    st.subheader("✨ Features")

    st.markdown("""
    - 📘 **Explain a Topic** — Understand difficult topics step by step.
    - 📝 **Generate Study Notes** — Create organised notes for revision.
    - 🧠 **Generate Quiz Questions** — Test your understanding with practice questions.
    - 💬 **AI Study Chat** — Ask questions and get learning support.
    """)

    st.info(
        "💡 Tip: Choose a topic you are studying at university, "
        "then start with AI Study Tools or AI Study Chat."
    )
