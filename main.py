from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import aiohttp
import uvicorn
import os

app = FastAPI()
# Безопасно храним токен
BOT_TOKEN = os.environ.get("BOT_TOKEN", "ТВОЙ_ТОКЕН_ЗДЕСЬ")

@app.get("/")
async def root():
    return {"message": "Reward server for @rublcub_bot is running!"}

@app.get("/reward")
async def reward_endpoint(request: Request):
    user_id = request.query_params.get('user_id')
    
    if user_id:
        try:
            # Отправляем сообщение в бота о награде
            async with aiohttp.ClientSession() as session:
                await session.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": int(user_id),
                        "text": "✅ Спасибо за просмотр! +1 спин зачислен!"
                    }
                )
            print(f"Reward sent to user {user_id}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Возвращаем пользователя обратно в твоего бота
    return RedirectResponse(url="https://t.me/rublcub_bot")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)