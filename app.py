from auth import get_auth_url, get_tokens
from fit_data import get_health_data
from flask import Flask, request, redirect

app = Flask(__name__)
credentials_store = {}

@app.route("/")
def home():
    auth_url = get_auth_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    auth_code = request.args.get("code")
    creds = get_tokens(auth_code)
    user_id = "user123"  # В реальном приложении - из сессии
    credentials_store[user_id] = creds
    return "Аутентификация успешна! <a href='/health-data'>Получить данные</a>"

@app.route("/health-data")
def health_data():
    user_id = "user123"
    creds = credentials_store.get(user_id)
    
    if not creds or creds.expired:
        return "Требуется повторная аутентификация"
    
    health_data = get_health_data(creds)
    return generate_ai_response(health_data)

def generate_ai_response(data):
    # Здесь ваш AI-агент анализирует данные
    response = []
    
    if data["steps"] < 8000:
        response.append(f"🔔 Сегодня вы прошли {data['steps']} шагов. Попробуйте сделать небольшую прогулку!")
    
    if data["avg_heart_rate"] > 85:
        response.append(f"⚠️ Ваш средний пульс {data['avg_heart_rate']} уд/мин. Рекомендую отдохнуть.")
    
    if data["sleep_duration"] < 7:
        response.append(f"😴 Вы спали всего {data['sleep_duration']} часов. Старайтесь спать 7-9 часов!")
    
    return "<br>".join(response) if response else "✅ Ваши показатели в норме!"

if __name__ == "__main__":
    app.run(port=8080, debug=True)