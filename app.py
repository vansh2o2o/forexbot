import streamlit as st
from pathlib import Path
from flask import Flask, request, jsonify
import requests
from bot_core import get_response, get_stock_examples, get_forex_examples
from config.settings import (
    APP_TITLE,
    TAGLINE,
    DISCLAIMER,
    QUICK_TIPS_STOCKS,
    QUICK_TIPS_FOREX,
)

# ---------- PATHS ----------
BASE_DIR = Path(__file__).resolve().parent
FAQ_PATH = BASE_DIR / "data" / "faq.md"

# Load FAQ text
if FAQ_PATH.exists():
    FAQ_TEXT = FAQ_PATH.read_text(encoding="utf-8")
else:
    FAQ_TEXT = "FAQ file not found. Please check data/faq.md"

# ---------- SIMPLE QUIZ DATA ----------
QUIZ_QUESTIONS = [
    {
        "question": "What does PE ratio basically compare?",
        "options": [
            "Price to Earnings",
            "Price to Equity",
            "Profit to Equity",
            "Price to Expense",
        ],
        "answer": "Price to Earnings",
        "explain": "PE = Price / Earnings per share. It shows how much you pay for ₹1 of earnings.",
    },
    {
        "question": "In a candlestick, what does the body represent?",
        "options": [
            "Difference between high and low",
            "Difference between open and close",
            "Only the closing price",
            "Only the highest price",
        ],
        "answer": "Difference between open and close",
        "explain": "The body of a candle is formed between the open and close prices.",
    },
    {
        "question": "What is a pip in most forex pairs (like EUR/USD)?",
        "options": [
            "0.01",
            "0.0001",
            "1.0",
            "0.1",
        ],
        "answer": "0.0001",
        "explain": "For most pairs, 1 pip = 0.0001 change in price.",
    },
    {
        "question": "What is the main purpose of a stop-loss?",
        "options": [
            "Increase profit",
            "Avoid tax",
            "Limit loss",
            "Get bonus lots",
        ],
        "answer": "Limit loss",
        "explain": "Stop-loss is primarily used to limit risk and protect capital.",
    },
    {
        "question": "Which two sessions usually create the highest forex volatility?",
        "options": [
            "Sydney & Tokyo",
            "Tokyo & London",
            "London & New York",
            "New York & Sydney",
        ],
        "answer": "London & New York",
        "explain": "The overlap of London and New York sessions often has strongest movement.",
    },
]

# ------------- STREAMLIT CONFIG -------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout="centered",
)

# ------------- SIDEBAR -------------
with st.sidebar:
    st.markdown(f"### {APP_TITLE}")
    st.caption(TAGLINE)
    st.markdown("---")

    st.markdown("#### 🔍 Quick Topic Buttons")

    # Quick stock topic buttons
    st.markdown("**Stocks (India)**")
    stock_buttons = {
        "PE & PB basics": "Explain PE and PB ratio in simple words",
        "Candlestick basics": "What is a candlestick chart and basic patterns?",
        "Support & Resistance": "Explain support and resistance levels",
        "Stop-loss & Target": "How to use stop-loss and set targets?",
    }
    for label, prompt in stock_buttons.items():
        if st.button(label, key=f"stock_{label}"):
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"role": "user", "content": prompt})
            reply = get_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

    st.markdown("**Forex**")
    forex_buttons = {
        "What is Forex?": "What is forex and how does it work?",
        "Pairs, pips & lots": "Explain forex pairs, pips and lots",
        "Sessions": "What are forex market sessions?",
        "Risk management": "Explain risk management in forex and stocks",
    }
    for label, prompt in forex_buttons.items():
        if st.button(label, key=f"forex_{label}"):
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"role": "user", "content": prompt})
            reply = get_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

    st.markdown("---")
    st.markdown("#### 📌 Quick References")

    with st.expander("📈 Popular Indian Stocks"):
        st.markdown(
            "Here are some example NSE/BSE symbols you can learn about (not live prices):"
        )
        st.code(", ".join(get_stock_examples()), language="text")

    with st.expander("💱 Common Forex Pairs"):
        st.markdown("Some major and INR-related currency pairs:")
        st.code(", ".join(get_forex_examples()), language="text")

    st.markdown("---")
    st.markdown("#### ⚙️ Session Controls")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset Chat"):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🚪 Exit App"):
            st.stop()

    st.markdown("---")
    st.caption(DISCLAIMER)

# ------------- MAIN AREA (TABS) -------------
st.title("📉📈 ShareBot – Learn Stocks & Forex")

tabs = st.tabs(["💬 Chatbot", "📚 Quick Guides", "❓ FAQ", "📝 Quiz"])

# ---------- TAB 1: CHATBOT ----------
with tabs[0]:
    st.markdown(
        "Ask me about **Indian stock market basics, charts, PE/PB, forex pairs, pips, risk management** etc."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi 👋, I’m your learning buddy for **Indian Share Market & Forex**.\n\n"
                    "You can ask things like:\n"
                    "- What is PE and PB ratio?\n"
                    "- Basics of candlestick chart?\n"
                    "- What is forex and what are major pairs?\n"
                    "- Explain pips, lots and spread.\n"
                    "- How to manage risk in trading?\n"
                    "\nYou can also type **exit / quit / bye / close** to end the session."
                ),
            }
        ]

    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_prompt = st.chat_input("Type your question here...", key="main_chat_input")

    if user_prompt:
        # ---- EXIT COMMANDS ----
        if user_prompt.strip().lower() in ["exit", "quit", "bye", "close"]:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "👋 **Goodbye! Trade Safely!! .**\n\nYou may now close this tab or restart the app.",
                }
            )

            with st.chat_message("assistant"):
                st.markdown("👋 **Goodbye! Trade safely!!.**")

            st.stop()

        # ---- NORMAL CHAT HANDLING ----
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        reply = get_response(user_prompt)
        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.markdown(reply)

# ---------- TAB 2: QUICK GUIDES ----------
with tabs[1]:
    st.markdown("### 📚 Quick Guides – At a Glance")

    st.markdown("#### 📈 Stocks – Key Points")
    for tip in QUICK_TIPS_STOCKS:
        st.markdown(f"- {tip}")

    st.markdown("---")
    st.markdown("#### 💱 Forex – Key Points")
    for tip in QUICK_TIPS_FOREX:
        st.markdown(f"- {tip}")

    st.markdown("---")
    st.info(
        "Use the **Chatbot** tab to ask detailed questions. "
        "These guides are just summary bullets."
    )

# ---------- TAB 3: FAQ ----------
with tabs[2]:
    st.markdown("### ❓ Frequently Asked Questions")
    st.markdown(FAQ_TEXT)

# ---------- TAB 4: QUIZ ----------
with tabs[3]:
    st.markdown("### 📝 Quick Quiz – Test Your Basics")

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = 0

    # Render questions
    for idx, q in enumerate(QUIZ_QUESTIONS):
        st.markdown(f"**Q{idx+1}. {q['question']}**")
        st.radio(
            "Select an answer:",
            q["options"],
            key=f"quiz_q_{idx}",
            label_visibility="collapsed",
        )
        st.markdown("---")

    if st.button("✅ Check Score"):
        score = 0
        explanations = []
        for idx, q in enumerate(QUIZ_QUESTIONS):
            user_ans = st.session_state.get(f"quiz_q_{idx}")
            correct = q["answer"]
            if user_ans == correct:
                score += 1
            explanations.append(
                f"Q{idx+1}: Correct answer: **{correct}**"
                f"<br/>Your answer: **{user_ans}**"
                f"<br/>{q['explain']}"
            )

        st.session_state.quiz_submitted = True
        st.session_state.quiz_score = score

        st.success(f"Your score: {score} / {len(QUIZ_QUESTIONS)}")
        with st.expander("View explanations"):
            for e in explanations:
                st.markdown(e, unsafe_allow_html=True)

    if st.session_state.get("quiz_submitted", False):
        st.info(
            "You can change your answers and press **Check Score** again to re-check."
        )

app = Flask(__name__)

def search_duckduckgo(query):
    url = f'https://api.duckduckgo.com/?q={query}&format=json&no_html=1'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    answer = data.get('AbstractText') or data.get('Answer')
    if answer:
        return answer
    related = data.get('RelatedTopics', [])
    if related and isinstance(related, list):
        for topic in related:
            if isinstance(topic, dict) and topic.get('Text'):
                return topic['Text']
    return 'No direct answer found.'

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    # First, try to answer from local knowledge base
    kb_answer = get_response(question)
    if kb_answer and 'No direct answer found.' not in kb_answer:
        return jsonify({'answer': kb_answer})
    # If not found, search the web
    search_query = f"{question} Indian stock market forex market"
    web_answer = search_duckduckgo(search_query)
    return jsonify({'answer': web_answer})

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)