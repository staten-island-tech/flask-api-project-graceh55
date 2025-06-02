from flask import Flask, render_template, request
import requests

app = Flask(__name__)

DISNEY_API_URL = "https://api.disneyapi.dev/character"

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    response = requests.get(DISNEY_API_URL, params={'page': page})
    data = response.json()
    characters = data.get('data', [])
    next_page = data.get('info', {}).get('nextPage', None)
    return render_template('index.html', characters=characters, next_page=next_page)

@app.route('/character/<int:character_id>')
def character(character_id):
    response = requests.get(f"{DISNEY_API_URL}/{character_id}")
    data = response.json()
    character = data.get('data', {})  # Fix here: single character is a dict, not list
    return render_template('disney.html', character=character)

if __name__ == '__main__':
    app.run(debug=True)