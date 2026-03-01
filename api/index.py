from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64

app = FastAPI()

# Разрешаем доступ для твоего приложения
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Вот твоя секретная строка
SECRET_KEY_HASH = "Z3NrX0Y1OGRPakxndjhaUFFISE1VY2x5V0dkeWIzRllVSFpISXpLRWFTQVh6RUpFak40a09hamY="

@app.post("/chat")
async def chat(data: dict):
    user_text = data.get("text", "")
    user_role = data.get("role", "base")
    
    # Дешифровка ключа в памяти сервера
    try:
        api_key = base64.b64decode(SECRET_KEY_HASH).decode('utf-8')
    except Exception:
        return {"error": "Ошибка ключа"}
    
    # Модели для Базовых и Hyper юзеров
    model_name = "llama-3.3-70b-specdec" if user_role == "base" else "llama-4-latests"
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "Ты Atlas AI от команды N.E.S из 142 школы. Учишь коду."},
            {"role": "user", "content": user_text}
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
