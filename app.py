from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load Apriori rules
with open('C:/Users/sunil/Desktop/ML APRIORI/Dataset14-Grocery-MarketBasket-Analysis.pkl', 'rb') as f:
    rules = pickle.load(f)

def suggest_items(item_name):
    item_name = item_name.strip().lower()
    recommendations = set()
    for _, rule in rules.iterrows():
        antecedents = [a.lower() for a in list(rule['antecedents'])]
        consequents = [c.lower() for c in list(rule['consequents'])]
        if item_name in antecedents:
            recommendations.update(consequents)
    return list(recommendations)[:6]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    item = request.args.get('item')
    if not item:
        return jsonify({'error': 'Please provide an item name.'}), 400
    suggestions = suggest_items(item)
    return jsonify({'input_item': item, 'recommended_items': suggestions})

if __name__ == '__main__':
    app.run(debug=True)
