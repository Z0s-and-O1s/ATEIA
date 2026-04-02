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

manager = ConversationManager()

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message
    session_id = request.session_id

    conn = get_connection()
    cursor = conn.cursor()

    # ✅ Save USER message
    cursor.execute(
        "INSERT INTO messages (session_id, sender, content) VALUES (?, ?, ?)",
        (session_id, "user", message)
    )

    stage = manager.get_stage()

    if stage == "AWAITING_ERROR":

        parsed = detect_language_and_parse(message)
        manager.receive_error(message)

        context_message = generate_context_request(
            parsed["language"], parsed["error_type"]
        )

        response = (
            f"Detected Language: {parsed['language']}\n"
            f"Error Type: {parsed['error_type']}\n\n"
            f"{context_message}"
        )

    elif stage == "AWAITING_CODE":

        manager.receive_code(message)

        parsed = detect_language_and_parse(manager.error_message)

        explanation = generate_explanation(
            manager.error_message,
            manager.code_snippet
        )

        response = format_debug_response(
            parsed["language"],
            parsed["error_type"],
            explanation
        )

    else:
        response = "Please reset the conversation and start again."

    # ✅ Save ASSISTANT response
    cursor.execute(
        "INSERT INTO messages (session_id, sender, content) VALUES (?, ?, ?)",
        (session_id, "assistant", response)
    )

    conn.commit()
    conn.close()

    return {"reply": response}

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