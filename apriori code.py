import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

df = pd.read_csv('C:/Users/sunil/Desktop/ML APRIORI/Dataset14-Grocery-MarketBasket-Analysis.csv') 

df = df.drop_duplicates() # remove duplicates

# Create transaction table / ye basket matric mei change krta hai data ko 
trans_df = pd.crosstab(df['Member_number'], df['itemDescription']).reset_index()
trans_df = trans_df.set_index('Member_number')

def encode_units(x):
    return 1 if x >= 1 else 0
basket_trans = trans_df.map(encode_units).astype(bool)   

frequent_itemsets = apriori(basket_trans, min_support=0.02, use_colnames=True) # Apply Apriori calculate support

rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0) # association rules

rules = rules.sort_values(['lift', 'support'], ascending=[False, False]).reset_index(drop=True)

def suggest_items(item_name):
    item_name = item_name.strip().lower()
    recommendations = set()
    for _, rule in rules.iterrows():
        antecedents = [a.lower() for a in list(rule['antecedents'])] # Convert to lowercase for consistency
        consequents = [c.lower() for c in list(rule['consequents'])]

        if item_name in antecedents:
            recommendations.update(consequents)
    return sorted(recommendations)[:6]  #top 6 suggestions

import pickle
with open('C:/Users/sunil/Desktop/ML APRIORI/Dataset14-Grocery-MarketBasket-Analysis.pkl', 'wb') as f:
    pickle.dump(rules, f)
