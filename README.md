Forked from techwithtim/LocalAIAgentWithRAG

# The Great Debate: Humanism vs AI

This chatbot was created for a midterm assignment for **02.137DH Introduction to Digital Humanities (SUTD)**.

The project explores philosophical debate between **Humanism** and **Post-Humanism**, where users challenge an AI that defends the value of human intelligence, experience, and moral reasoning.

Users take the role of the **Post Humanist challenger**, while the AI responds as a **Humanist debater**.

The system combines retrieval augmented generation, speech recognition, and speech synthesis to create a dynamic interactive debate experience.

---

# Features

- Humanist AI debate agent powered by a local language model
- Retrieval augmented responses using relevant article excerpts
- Voice input using speech to text
- AI responses delivered through text to speech
- Debate hall themed user interface built with Streamlit
- Interactive chat interface for structured debate

---

# Tech Stack

- **Python 3.11**
- **Streamlit** — interactive web interface
- **LangChain** — LLM orchestration
- **Ollama** — local LLM inference
- **RAG (Retrieval Augmented Generation)** — contextual knowledge retrieval
- **Speech Recognition** — speech to text
- **Text to Speech** — AI voice responses

---

# System Requirements

- Python **3.11**
- Ollama installed and running locally
- Git (optional but recommended)

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd <project-folder>

---
```

## 2. Create a virtual environment

Create a Python virtual environment using Python 3.11.

```bash
python3.11 -m venv venv

```

## For Mac/Linux
```bash
source venv/bin/activate
```

## For Windows
```bash
venv\Scripts\activate
```

## 3. Install all the credentials
```bash
pip install -r requirements.txt
```

## 4. Run Streamlit
```bash
Streamlit run app.py
```
