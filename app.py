import streamlit as st
from vector import retriever
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from stt import listen
from tts import speak


st.set_page_config(
    page_title="The Great Debate: Humanism vs AI",
    page_icon="⚖️",
    layout="wide"
)


st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #1a0000, #000000);
    color: #f5f5f5;
    font-family: Georgia, serif;
}

header {visibility:hidden;}
footer {visibility:hidden;}

.block-container {
    padding-top: 2rem;
}



.debate-stage {
    background: linear-gradient(180deg,#330000 0%,#000000 100%);
    padding:2rem;
    border-radius:18px;
    border:2px solid #ff3b3b;
    box-shadow:0 0 25px rgba(255,0,0,0.4);
    text-align:center;
    margin-bottom:1.5rem;
}

.debate-title {
    font-size:3rem;
    font-weight:bold;
    color:#ff4b4b;
    letter-spacing:3px;
    text-shadow:0 0 15px rgba(255,0,0,0.7);
}

.debate-subtitle {
    color:#bbbbbb;
    font-style:italic;
    font-size:1.1rem;
}


.podium {
    padding:1.6rem;
    border-bottom:6px solid #ff3b3b;
    background:rgba(255,50,50,0.06);
    border-radius:12px 12px 0 0;
    text-align:center;
    margin-top:1rem;
    box-shadow:0 5px 15px rgba(0,0,0,0.6);
    transition:all 0.25s ease;
}

.podium:hover {
    transform:translateY(-3px);
    box-shadow:0 0 18px rgba(255,0,0,0.5);
}

.podium-label {
    color:#ff4b4b;
    font-weight:bold;
    font-size:0.9rem;
    text-transform:uppercase;
    letter-spacing:1px;
}

.podium-name {
    font-size:1.6rem;
    margin-top:0.5rem;
    color:#ffffff;
}


.stChatMessage {
    background:rgba(255,255,255,0.04) !important;
    border-radius:12px !important;
    border:1px solid rgba(255,70,70,0.3) !important;
    padding:1rem !important;
}

/* Opponent message */

[data-testid="stChatMessage"]:nth-child(odd) {
    border-left:5px solid #3498db !important;
}

/* Humanist reply */

[data-testid="stChatMessage"]:nth-child(even) {
    border-right:5px solid #ff3b3b !important;
    background:rgba(255,0,0,0.08) !important;
}


.stButton > button {
    background:#1a0000 !important;
    color:#ff4b4b !important;
    border:1px solid #ff3b3b !important;
    font-weight:bold;
    transition:all 0.2s ease;
}

.stButton > button:hover {
    background:#ff3b3b !important;
    color:#000000 !important;
    box-shadow:0 0 10px rgba(255,0,0,0.6);
}



::-webkit-scrollbar {
    width:8px;
}

::-webkit-scrollbar-thumb {
    background:#ff3b3b;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)



st.markdown("""
<div class="debate-stage">
    <div class="debate-title">The Great Hall</div>
    <div class="debate-subtitle">
        Human Consciousness vs Algorithmic Logic
    </div>
</div>
""", unsafe_allow_html=True)



col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="podium">
        <div class="podium-label">Challenger</div>
        <div class="podium-name">The Post-Humanist</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="podium">
        <div class="podium-label">Defender</div>
        <div class="podium-name">The Humanist</div>
    </div>
    """, unsafe_allow_html=True)



if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_spoken_message" not in st.session_state:
    st.session_state.last_spoken_message = None



try:
    model = OllamaLLM(
        model="llama3.2",
        num_predict=400,
        temperature=0.6
    )
except Exception as e:
    st.error(f"Ollama error: {e}")
    model = None


template = """
You are a confident humanist debater arguing against the idea that machines or artificial intelligence will surpass human intelligence.

The user may present arguments supporting post-humanism. Your role is to challenge their claims directly and defend the humanist position.

Guidelines for your response:
- Speak directly to the user, not about them.
- Do not say phrases like "my opponent argues".
- Respond naturally, like you are debating the user in a conversation.
- Question the assumptions behind the user's claim.
- Emphasize uniquely human qualities such as empathy, moral judgment, lived experience, cultural meaning, and creativity rooted in human life.

Debate strategy:
1. Briefly address the user's claim.
2. Point out the hidden assumption or weakness in it.
3. Reframe the argument from a humanist perspective.

Use these article excerpts as supporting ideas when relevant:

{articles}

User statement:
{question}

Write about 6–7 sentences. Speak confidently and directly to the user. End with a clear conclusion that human intelligence and experience cannot be replaced by artificial intelligence.
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model if model else None


# ---------------- BOT FUNCTION ----------------
def ask_bot(question):

    if not chain:
        return "Model unavailable."

    try:

        docs = retriever.invoke(question)

        articles = "\n\n".join([d.page_content for d in docs])

        result = chain.invoke({
            "articles": articles,
            "question": question
        })

        return str(result).strip()

    except Exception as e:
        return f"Error: {e}"


chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])



user_input = st.chat_input(
    "Present your argument to the Humanist..."
)



st.divider()

col1, col2 = st.columns(2)

with col1:
    voice_button = st.button(
        "🎤 Voice Input",
        use_container_width=True
    )

with col2:
    clear_button = st.button(
        "🗑 Clear Stage",
        use_container_width=True
    )



question = None

if user_input:
    question = user_input

elif voice_button:
    try:
        with st.spinner("Listening..."):
            question = listen()
    except Exception as e:
        st.error(e)


if clear_button:
    st.session_state.messages = []
    st.session_state.last_spoken_message = None
    st.rerun()



if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with chat_container:

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("The Humanist is thinking..."):
                answer = ask_bot(question)
                st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


    # speak response
    if st.session_state.last_spoken_message != answer:
        try:
            speak(answer)
            st.session_state.last_spoken_message = answer
        except Exception as e:
            st.error(e)

    st.rerun()