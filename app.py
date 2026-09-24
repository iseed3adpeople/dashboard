import json
from datetime import datetime
from pathlib import Path

import requests
from flask import Flask, redirect, render_template, request, url_for

from config import API_KEY, BIRTHDAY, CITY

app = Flask(__name__)

GOALS_FILE = Path(__file__).parent / "goals.json"


def load_goals():
    with open(GOALS_FILE, encoding="utf-8") as file:
        return json.load(file)


def save_goals(goals):
    with open(GOALS_FILE, "w", encoding="utf-8") as file:
        json.dump(goals, file, ensure_ascii=False, indent=2)


def greeting_for_hour(hour):
    if 6 <= hour < 12:
        return "Good morning", "☕"
    if 12 <= hour < 18:
        return "Good afternoon", "💻"
    if 18 <= hour < 24:
        return "Good evening", "🌙"
    return "Good night", "😴"


@app.route("/")
def index():
    now = datetime.now()
    greeting, icon = greeting_for_hour(now.hour)
    days_left = (BIRTHDAY - now).days + 1

    weather_url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={API_KEY}&units=metric&lang=en"
    )
    weather = requests.get(weather_url, timeout=5).json()

    return render_template(
        "index.html",
        days=days_left,
        temperature=weather["main"]["temp"],
        description=weather["weather"][0]["description"],
        weather_type=weather["weather"][0]["main"],
        greeting=greeting,
        icon=icon,
        goals=load_goals(),
    )


@app.route("/toggle_goal/<int:goal_id>", methods=["POST"])
def toggle_goal(goal_id):
    goals = load_goals()
    for goal in goals:
        if goal["id"] == goal_id:
            goal["completed"] = not goal["completed"]
            break
    save_goals(goals)
    return "ok"


@app.route("/add_goal", methods=["POST"])
def add_goal():
    goal_text = request.form["goal_text"]
    goals = load_goals()
    new_id = max((g["id"] for g in goals), default=0) + 1
    goals.append({"id": new_id, "text": goal_text, "completed": False})
    save_goals(goals)
    return redirect(url_for("index"))


@app.route("/delete_goal/<int:goal_id>", methods=["POST"])
def delete_goal(goal_id):
    goals = [g for g in load_goals() if g["id"] != goal_id]
    save_goals(goals)
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
