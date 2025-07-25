from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = "620fcbb0770d4c2cc412be3c845cb784"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city.title()} is {weather} with a temperature of {temp}°C."
    elif response.status_code == 404:
        return "City not found. Please enter a valid city name."
    else:
        return "Sorry, couldn't fetch weather data right now."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_input = request.form["msg"]
    if "weather" in user_input.lower():
        city = user_input.lower().replace("weather in", "").strip()
        reply = get_weather(city)
    else:
        reply = "Please ask about the weather using format like: 'What’s the weather in London?'"
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
