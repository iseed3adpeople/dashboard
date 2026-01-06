from flask import Flask, render_template, request, redirect, url_for
from datetime import *
from config import bd, API_KEY, CITY
import requests
import json

app = Flask(__name__)


@app.route('/')
def index():
    now = datetime.now()
    hour = now.hour

    if 6 <= hour < 12:
        greeting = 'Good morning'
        icon = "☕"
    elif 12 <= hour < 18:
        greeting = 'Good afternoon'
        icon = "💻"
    elif 18 <= hour < 24:
        greeting = 'Good evening'
        icon = "🌙"
    else:
        greeting = 'Good night'
        icon = "😴"

    delta = bd - now
    days = delta.days + 1

    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=en"
    response = requests.get(url)
    data = response.json()

    temperature = data['main']['temp']
    weather_type = data['weather'][0]['main']
    description = data['weather'][0]['description']

    with open('goals.json', 'r', encoding='utf-8') as file:
        goals = json.load(file)

    return render_template(
        'index.html',
        days=days,
        temperature=temperature,
        description=description,
        weather_type=weather_type,
        greeting=greeting,
        icon=icon,
        goals=goals
    )


@app.route('/toggle_goal/<int:goal_id>', methods=['GET', 'POST'])
def toggle_goal(goal_id):
    with open('goals.json', 'r', encoding='utf-8') as file:
        goals = json.load(file)

    for goal in goals:
        if goal['id'] == goal_id:
            goal['completed'] = not goal['completed']
            break

    with open('goals.json', 'w', encoding='utf-8') as file:
        json.dump(goals, file, ensure_ascii=False, indent=2)

    return 'ok'


@app.route('/add_goal', methods=['POST'])
def add_goal():
    goal_text = request.form['goal_text']

    with open('goals.json', 'r', encoding='utf-8') as file:
        goals = json.load(file)

    new_id = max([g['id'] for g in goals] + [0]) + 1
    goals.append({'id': new_id, 'text': goal_text, 'completed': False})

    with open('goals.json', 'w', encoding='utf-8') as file:
        json.dump(goals, file, ensure_ascii=False, indent=2)

    return redirect(url_for('index'))


@app.route("/delete_goal/<int:goal_id>", methods=['POST'])
def delete_goal(goal_id):
    with open('goals.json', 'r', encoding='utf-8') as file:
        goals = json.load(file)

    new_goals = [g for g in goals if g['id'] != goal_id]

    with open('goals.json', 'w', encoding='utf-8') as file:
        json.dump(new_goals, file, ensure_ascii=False, indent=2)
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)