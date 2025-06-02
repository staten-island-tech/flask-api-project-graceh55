from flask import Flask, request, jsonify
import requests
import json
import os
import re

app = Flask(__name__)

# Replace with your real Edamam credentials
EDAMAM_APP_ID = "your_real_app_id"
EDAMAM_API_KEY = "your_real_app_key"

def clean_filename(title):
    # Create a safe filename: lowercase, underscores, no special characters
    filename = re.sub(r'[^a-zA-Z0-9_]', '', title.replace(' ', '_').lower())
    return filename + ".json"

@app.route('/')
def home():
    return "Edamam Nutrition API is running. Use POST /analyze_recipe"

@app.route('/analyze_recipe', methods=['POST'])
def analyze_recipe():
    data = request.get_json()

    if not data or 'title' not in data or 'ingr' not in data:
        return jsonify({"error": "Missing 'title' or 'ingr' in request"}), 400

    url = "https://api.edamam.com/api/nutrition-details"
    params = {
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_API_KEY
    }

    try:
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        result = response.json()

        # Generate safe filename from recipe title
        filename = clean_filename(data['title'])
        output_path = os.path.join(os.getcwd(), filename)

        with open(output_path, "w") as f:
            json.dump(result, f, indent=4)

        return jsonify({
            "message": f"Nutrition data saved to {filename}",
            "summary": {
                "calories": result.get("calories"),
                "totalWeight": result.get("totalWeight"),
                "dietLabels": result.get("dietLabels", []),
                "healthLabels": result.get("healthLabels", [])
            }
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "API request failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



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