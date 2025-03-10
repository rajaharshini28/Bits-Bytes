from flask import Flask, render_template, request, jsonify
import requests
import random

app = Flask(__name__)

# Spoonacular API configuration
API_KEY = 'eedca747e7cd4d0290573202e7fe05c6'  # Replace with your actual API key
BASE_URL = 'https://api.spoonacular.com/recipes'

def generate_recipe(preferences):
    # Create a query string from user preferences
    ingredients = ','.join(preferences)
    url = f"{BASE_URL}/findByIngredients?ingredients={ingredients}&apiKey={API_KEY}"

    # Make a request to the Spoonacular API
    response = requests.get(url)
    if response.status_code == 200:
        recipes = response.json()
        if recipes:
            # Randomly select a recipe from the results
            selected_recipe = random.choice(recipes)
            recipe_details_url = f"{BASE_URL}/{selected_recipe['id']}/information?apiKey={API_KEY}"
            recipe_details_response = requests.get(recipe_details_url)
            recipe_details = recipe_details_response.json()

            # Create a structured recipe response
            recipe = {
                "title": recipe_details['title'],
                "ingredients": [ingredient['name'] for ingredient in recipe_details['extendedIngredients']],
                "instructions": recipe_details['instructions'] if 'instructions' in recipe_details else "No instructions available."
            }
            return recipe
        else:
            return {"message": "No recipes found matching your preferences."}
    else:
        return {"message": "Error fetching recipes from the API."}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_preferences = request.json.get('preferences', [])
    recipe = generate_recipe(user_preferences)
    return jsonify(recipe)

if __name__ == '__main__':
    app.run(debug=True)