import matplotlib
matplotlib.use('Agg')    
from flask import Flask, request, jsonify, render_template, send_file
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import io
import os

app = Flask(__name__)

# Load Apriori rules
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pkl_path = os.path.join(BASE_DIR, 'Dataset14-Grocery-MarketBasket-Analysis.pkl')
with open(pkl_path, 'rb') as f:
    rules = pickle.load(f)

def suggest_items(item_name):
    item_name = item_name.strip().lower()
    recommendations = set() # in set datatype to have only unique values
    for _, rule in rules.iterrows():
        antecedents = [a.lower() for a in list(rule['antecedents'])]
        consequents = [c.lower() for c in list(rule['consequents'])]
        if item_name in antecedents:
            recommendations.update(consequents)
    return list(recommendations)[:6]

# BAR CHART 

def generate_reco_bar_chart(recommended_items):
    recommended_items = [i.lower() for i in recommended_items]

    item_counts = {}

    for _, row in rules.iterrows():
        for item in row['antecedents']:
            item = item.lower()
            if item in recommended_items:
                item_counts[item] = item_counts.get(item, 0) + 1

    df = pd.DataFrame(list(item_counts.items()), columns=['Item', 'Count'])
    df = df.sort_values(by='Count', ascending=True)

    # Dynamic figure height based on number of items for perfect vertical spacing
    num_items = len(df)
    fig_height = max(3.5, num_items * 0.7 + 1.2)
    fig, ax = plt.subplots(figsize=(9.5, fig_height), dpi=150)

    if not df.empty:
        bars = ax.barh(df['Item'].str.title(), df['Count'], color="#078b2d", height=0.55, edgecolor="#05681e")
        # Direct value labels on each bar
        ax.bar_label(bars, padding=6, fontsize=11, fontweight="bold", color="#078b2d")
        ax.set_xlim(0, max(df['Count']) * 1.15)

    ax.set_xlabel("Occurrence Frequency in Rules", fontsize=12, fontweight="bold", color="#2d3748", labelpad=10)
    ax.set_ylabel("Item Name", fontsize=12, fontweight="bold", color="#2d3748", labelpad=10)
    ax.set_title("Recommended Items Frequency Comparison", fontsize=15, fontweight="bold", color="#078b2d", pad=14)

    # Make item names and numbers large and readable
    ax.tick_params(axis='y', labelsize=12, colors='#1a202c')
    for label in ax.get_yticklabels():
        label.set_fontweight('bold')

    ax.tick_params(axis='x', labelsize=11, colors='#4a5568')

    # Clean borders and grid
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cbd5e0')
    ax.spines['bottom'].set_color('#cbd5e0')
    ax.xaxis.grid(True, linestyle='--', alpha=0.5, color='#e2e8f0')
    ax.set_axisbelow(True)

    fig.tight_layout()

    # Save to buffer
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    return buffer



@app.route('/reco_bar_chart')
def reco_bar_chart():
    item = request.args.get('item')

    if not item:
        return "Item not provided", 400

    recommended_items = suggest_items(item)
    img = generate_reco_bar_chart(recommended_items)

    return send_file(img, mimetype='image/png')

         

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


