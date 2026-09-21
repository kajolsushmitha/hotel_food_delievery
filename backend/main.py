import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.controller.pass_controller import router as passenger_router
from backend.controller.hotel_controller import router as hotel_router
from backend.controller.menu_controller import router as menu_router
from backend.controller.order_controller import router as order_router
from backend.controller.history_controller import router as order_history_router
from backend.controller.auth_controller import (
    router as auth_router,
    hotel_auth_router
)
from backend.services.ttl_service import ttl_cleanup_worker
from backend.controller.chatbot_controller import router as chatbot_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    ttl_task = asyncio.create_task(ttl_cleanup_worker())
    yield
    ttl_task.cancel()
    try:
        await ttl_task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="Hotel Food Ordering API",
    lifespan=lifespan
)

app.include_router(passenger_router)
app.include_router(hotel_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(order_history_router)
app.include_router(auth_router)
app.include_router(hotel_auth_router)
app.include_router(chatbot_router)

@app.get("/")
def home():
    return {
        "message": "Hotel Food Ordering API is running"
    }