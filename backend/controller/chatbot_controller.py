from fastapi import APIRouter
from backend.schema.chatbot_schema import (
    ChatRequest,
    ChatResponse
)
from backend.services.chatbot_service import (
    chat_with_hotel_menu
)

router = APIRouter(
    prefix="/api/chat",
    tags=["Chatbot"]
)


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = chat_with_hotel_menu(
        message=request.message
    )

    return ChatResponse(
        user_message=request.message,
        response=response
    )