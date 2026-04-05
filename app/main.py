from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from db.models import create_tables
from db.database import get_connection
from core.conversation_manager import ConversationManager
from core.error_parser.parser_router import detect_language_and_parse
from schemas.chat_request import ChatRequest
from core.context_engine import generate_context_request
from ai.ai_engine import generate_explanation
from core.response_formatter import format_debug_response

app = FastAPI()

create_tables()

session_managers = {}

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    import os

    message = request.message
    session_id = request.session_id

    # ✅ STEP 1 — SAVE USER MESSAGE
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (session_id, sender, content) VALUES (?, ?, ?)",
        (session_id, "user", message)
    )

    conn.commit()
    conn.close()

    # ✅ STEP 2 — FETCH HISTORY
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT sender, content FROM messages WHERE session_id = ? ORDER BY message_id DESC LIMIT 10",
        (session_id,)
    )

    history = cursor.fetchall()
    conn.close()

    messages = []

    # 🧠 SYSTEM PROMPT
    messages.append({
        "role": "system",
        "content": (
            "You are ATEIA, a smart, friendly coding assistant. "
            "Talk like a human mentor and help debug step-by-step."
        )
    })

    for msg in reversed(history):
        role = "user" if msg["sender"] == "user" else "assistant"
        messages.append({
            "role": role,
            "content": msg["content"]
        })

    # 🚀 TRY OPENAI (IF AVAILABLE)
    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content

    # 🧠 FALLBACK (NO API / QUOTA)
    except Exception as e:
        print("AI FAILED:", str(e))

        user_input = message.lower()

        if "error" in user_input:
            reply = "Hmm, looks like you're facing an error. Can you share the full error message or your code? I'll help you fix it step-by-step."

        elif "print(x)" in user_input:
            reply = "You're trying to use variable 'x' without defining it first. Try this:\n\nx = 10\nprint(x)"

        elif "typeerror" in user_input:
            reply = "This looks like a type mismatch. You might be combining incompatible types like int and string. Try converting them properly."

        elif "nameerror" in user_input:
            reply = "This means a variable is being used before it's defined. Make sure you assign a value before using it."

        elif "hi" in user_input or "hello" in user_input:
            reply = "Hey! 👋 I'm ATEIA. What are you working on today? Got any bugs I can help with?"

        else:
            reply = "Got it 👍 Tell me more about your issue or share your code. I'll help you debug it."

    # ✅ STEP 3 — SAVE ASSISTANT REPLY
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (session_id, sender, content) VALUES (?, ?, ?)",
        (session_id, "assistant", reply)
    )

    conn.commit()
    conn.close()

    return {"reply": reply}

@app.get("/reset")
def reset_chat():
    global manager
    manager = ConversationManager()
    return {"message": "Conversation reset"}

@app.post("/create_session")
def create_session():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO sessions DEFAULT VALUES")
    session_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {"session_id": session_id}

@app.get("/sessions")
def get_sessions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT session_id FROM sessions ORDER BY session_id DESC")
    rows = cursor.fetchall()

    conn.close()

    return [{"session_id": row["session_id"]} for row in rows]

@app.get("/messages/{session_id}")
def get_messages(session_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT sender, content FROM messages WHERE session_id = ? ORDER BY message_id",
        (session_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "sender": row["sender"],
            "content": row["content"]
        }
        for row in rows
    ]