from flask import Flask, render_template, request, redirect, url_for, abort, make_response
import requests

app = Flask(__name__)
DISNEY_API_BASE = "https://api.disneyapi.dev/character"


def fetch_all_characters():
    characters = []
    url = DISNEY_API_BASE
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            break
        data = response.json()
        characters.extend(data.get('data', []))
        url = data.get('nextPage') 

    return sorted(characters, key=lambda c: c['_id'])

@app.route('/')
def index():
    characters = fetch_all_characters()
    return render_template('index.html', disney=characters)

@app.route('/character/id/<int:id>')
def character_by_id(id):
    url = f"{DISNEY_API_BASE}/{id}"
    response = requests.get(url)
    if response.status_code != 200:
        abort(404)
    character_data = response.json().get("data")
    if not character_data:
        abort(404)
    return render_template('character.html', disney=character_data)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('index'))

    response = requests.get(DISNEY_API_BASE, params={'name': query})
    if response.status_code != 200:
        rendered = render_template('character.html', disney=None, error="Failed to fetch from API")
        resp = make_response(rendered)
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return resp

    data = response.json()
    characters = data.get('data', [])

    if not characters:
        rendered = render_template('character.html', disney=None, error=f"Character '{query}' not found.")
        resp = make_response(rendered)
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return resp

    if len(characters) == 1:
        character_id = characters[0].get('_id')
        if not character_id:
            rendered = render_template('character.html', disney=None, error="Character data is incomplete.")
            resp = make_response(rendered)
            resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            return resp
        return redirect(url_for('character_by_id', id=character_id))

    # Multiple results: show list page
    rendered = render_template('search_results.html', query=query, characters=characters)
    resp = make_response(rendered)
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return resp

if __name__ == '__main__':
    app.run(debug=True)
