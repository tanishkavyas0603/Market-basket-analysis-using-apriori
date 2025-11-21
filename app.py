import matplotlib
matplotlib.use('Agg')    
from flask import Flask, request, jsonify, render_template, send_file
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import io

app = Flask(__name__)

# Load Apriori rules
with open('C:/Users/sunil/Desktop/ML APRIORI/Dataset14-Grocery-MarketBasket-Analysis.pkl', 'rb') as f:
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

# NETWORK GRAPH
def generated_network_graph(input_item, recommended_items):
    G = nx.DiGraph()
    input_item = input_item.lower()

    # Build edges with lift values
    for _, row in rules.iterrows():
        antecedents = [a.lower() for a in list(row['antecedents'])]
        consequents = [c.lower() for c in list(row['consequents'])]

        if input_item in antecedents:
            for item in recommended_items:
                if item.lower() in consequents:
                    lift_value = round(row['lift'], 2)
                    G.add_edge(input_item, item.lower(), weight=lift_value)

    # Start a clean figure
    fig = plt.figure(figsize=(18,12))
    ax = fig.add_subplot(111)

    pos = nx.spring_layout(G, seed=42)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color="lightgreen" , node_size=15000, ax=ax)

    # Draw edges
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=14, edge_color="black", ax=ax)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=18,  font_color='black',font_weight="bold", ax=ax)

    # Edge weight labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_weight="bold", font_size=15 , ax=ax)

    ax.axis("off") # taki grid or axis na aaye network graph mein

    # Save image
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    return buffer



@app.route('/network-graph')
def network_graph():
    input_item=request.args.get('item')
    if not input_item:
        return "Item not provided",400
    recommended_items=suggest_items(input_item)
    img = generated_network_graph(input_item,recommended_items)
    return send_file(img, mimetype='image/png')

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

    # Clean new figure 
    fig = plt.figure(figsize=(18,12))
    ax = fig.add_subplot(111)

    ax.barh(df['Item'], df['Count'], color="#087D35")
    ax.set_xlabel("Number of time item occurred (Frequency)", fontsize=14, fontweight="bold")
    ax.set_ylabel("Item Name", fontsize=16, fontweight="bold")
    ax.set_title("Bar Chart for Comparison", fontsize=18, fontweight="bold") 

    # Save to buffer
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches="tight")
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
