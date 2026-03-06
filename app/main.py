from fastapi import FastAPI
from db.models import create_tables
from core.conversation_manager import ConversationManager
from core.error_parser.parser_router import detect_language_and_parse
from schemas.chat_request import ChatRequest
from core.context_engine import generate_context_request
from ai.ai_engine import generate_explanation
from core.response_formatter import format_debug_response

app = FastAPI()

create_tables()

manager = ConversationManager()

@app.get("/")
def home():
    return {"message": "ATEIA is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message

    if manager.get_stage() == "AWAITING_ERROR":
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

    elif manager.get_stage() == "AWAITING_CODE":

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
        response = "Analysis stage reached (AI will run here later)."

    return {"reply": response}

@app.get("/reset")
def reset_chat():
    global manager
    manager = ConversationManager()
    return {"message": "Conversation reset"}