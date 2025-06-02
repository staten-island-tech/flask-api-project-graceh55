from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace with your actual Edamam API credentials
EDAMAM_APP_ID = os.environ.get("EDAMAM_APP_ID", "your_app_id")
EDAMAM_API_KEY = os.environ.get("EDAMAM_API_KEY", "your_api_key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    ingredients = request.json.get('ingredients')
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    url = "https://api.edamam.com/api/nutrition-data"
    params = {
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_API_KEY,
        "ingr": ingredients
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "API request failed"}), 500

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')



""" from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    # Get the first 150 food from the API
    response = requests.get("https://api.edamam.com/doc/open-api/nutrition-analysis-v1.yaml")
    data = response.json()
    nutrition_list = data['results']
    
    # Create a list to hold food details
    nutritions = []
    
    for    nutrition in nutrition_list:
        # Each food URL looks like "https://api.edamam.com/doc/open-api/nutrition-analysis-v1.yaml"
        url =  nutrition['url']
        parts = url.strip("/").split("/")
        id = parts[-1]  # The last part is the food's ID
        
        # Create an image URL using the food's ID
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/nutrition/{id}.png"
        
        nutritions.append({
            'name':    nutrition['name'].capitalize(),
            'id': id,
            'image': image_url
        })
    
    # Send the food list to the index.html page
    return render_template("index.html",   nutritions= nutritions)

# New route: When a user clicks a food card, this page shows more details and a stats chart
@app.route("/  nutrition/<int:id>")
def    nutrition_detail(id):
    # Get detailed info for the food using its id
    response = requests.get(f"https://api.edamam.com/doc/open-api/nutrition-analysis-v1.yaml   nutrition/{id}")
    data = response.json()
    
    # Extract extra details like types, height, and weight
    types = [t['type']['name'] for t in data['types']]
    calories = data.get('calories')
    total_nutrients = data.get('total_nutrients')
    name = data.get('name').capitalize()
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/nutrition/{id}.png"
    
    # Extract base stats for the chart (e.g., hp, attack, defense, etc.)
    stat_names = [stat['stat']['name'] for stat in data['stats']]
    stat_values = [stat['base_stat'] for stat in data['stats']]
    
    # Send all details to the  nutrition.html template
    return render_template("   nutrition.html", nutrition={
        'name': name,
        'id': id,
        'image': image_url,
        'types': types,
        'calories': calories,
        'total_nutrients': total_nutrients

    })

if __name__ == '__main__':
    app.run(debug=True) """