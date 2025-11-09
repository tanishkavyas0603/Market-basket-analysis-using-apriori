import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Load dataset
df = pd.read_csv('C:/Users/sunil/Desktop/ML APRIORI/Dataset14-Grocery-MarketBasket-Analysis.csv')

# Clean duplicates
df = df.drop_duplicates()

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df = df.sort_values('Date')

# Create transaction table
trans_df = pd.crosstab(df['Member_number'], df['itemDescription']).reset_index()
trans_df = trans_df.set_index('Member_number')

# Encode data for Apriori
def encode_units(x):
    return 1 if x >= 1 else 0
basket_trans = trans_df.map(encode_units)

basket_trans = basket_trans.astype(bool)   


# Apply Apriori on the entire basket
frequent_itemsets = apriori(basket_trans, min_support=0.02, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

# Clean up rules
rules = rules.sort_values(['lift', 'support'], ascending=[False, False]).reset_index(drop=True)

# Create a clean function for suggestions
def suggest_items(item_name):
    item_name = item_name.strip().lower()
    recommendations = set()
    for _, rule in rules.iterrows():
        # Convert to lowercase for consistency
        antecedents = [a.lower() for a in list(rule['antecedents'])]
        consequents = [c.lower() for c in list(rule['consequents'])]

        if item_name in antecedents:
            recommendations.update(consequents)
    return list(recommendations)[:6]  # return top 6 suggestions

# ✅ Test
print("Suggestions for 'bread':", suggest_items('bread'))

# ✅ Save your trained rules for Flask
import pickle
with open('C:/Users/sunil/Desktop/ML APRIORI/Dataset14-Grocery-MarketBasket-Analysis.pkl', 'wb') as f:
    pickle.dump(rules, f)

print("✅ Apriori rules saved successfully!")
