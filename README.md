# 🛒 Grocery Recommendation System using Apriori Algorithm

A simple, practical Market Basket Analysis project built with Python and Flask. It analyzes a grocery transaction dataset using the **Apriori Algorithm** to find items that customers frequently purchase together, and displays recommendations alongside a comparison bar chart on a local web page.

---

## 📌 How the Project Works

The project consists of two main parts: an **offline rule generation script** and a **local web application**.

```
[Grocery Dataset (CSV)]
         │
         ▼
[apriori code.py]  ──>  Cleans data, builds customer basket matrix, runs Apriori
         │
         ▼
[Dataset14-...Analysis.pkl]  ──>  Stores calculated association rules
         │
         ▼
[app.py (Flask)]  ──>  Loads rules, serves web UI, generates recommendation bar chart
         │
         ▼
[Browser (localhost:5000)]  ──>  User enters an item, views suggestions & chart
```

1. **Rule Mining (`apriori code.py`)**:
   - Reads the grocery transactions from `Dataset14-Grocery-MarketBasket-Analysis.csv` (38,765 records).
   - Drops duplicate entries.
   - Reshapes the data using `pd.crosstab` into a customer-item binary table (whether a customer bought an item or not).
   - Uses `mlxtend.frequent_patterns.apriori` with a minimum support of `0.02` (2%) to find frequent itemsets.
   - Generates association rules filtered by `lift >= 1.0` and sorts them by lift and support.
   - Saves the final rules table into `Dataset14-Grocery-MarketBasket-Analysis.pkl`.

2. **Web Application (`app.py` & `templates/index.html`)**:
   - Loads the saved `.pkl` rules file on startup.
   - When a user enters an item name (e.g. `yogurt`, `rolls/buns`, `whole milk`):
     - Finds all matching rules where the entered item is an antecedent.
     - Collects up to 6 unique recommended products.
     - Generates a horizontal bar chart with **Matplotlib** comparing how often each recommended product appears in the rules.
     - Displays the product names in green cards and embeds the readable bar chart below them.

---

## 🧠 Core Metrics Explained

- **Support**: How frequently an item or itemset appears across all transactions.
  $$\text{Support}(A \rightarrow B) = \frac{\text{Count}(A \text{ and } B)}{\text{Total Transactions}}$$
- **Confidence**: How often item $B$ is bought when item $A$ is purchased.
  $$\text{Confidence}(A \rightarrow B) = \frac{\text{Support}(A \text{ and } B)}{\text{Support}(A)}$$
- **Lift**: Measures whether $A$ and $B$ are genuinely bought together more often than expected by chance.
  $$\text{Lift}(A \rightarrow B) = \frac{\text{Confidence}(A \rightarrow B)}{\text{Support}(B)}$$
  - **Lift > 1.0**: Positive relationship (buying $A$ increases the likelihood of buying $B$).
  - **Lift = 1.0**: No relationship (independent).
  - **Lift < 1.0**: Negative relationship (unlikely to be bought together).

---

## 📁 Repository Files

| File | Description |
| :--- | :--- |
| `Dataset14-Grocery-MarketBasket-Analysis.csv` | Raw grocery dataset containing `Member_number`, `Date`, and `itemDescription`. |
| `Dataset14-Grocery-MarketBasket-Analysis.pkl` | Pre-calculated association rules saved as a pickle file for fast lookups. |
| `apriori code.py` | Python script that cleans the CSV, runs the Apriori algorithm, and creates the `.pkl` file. |
| `app.py` | Local Flask server that handles item lookups and generates the dynamic Matplotlib bar chart. |
| `templates/index.html` | The web frontend with an input search box, suggestion cards, and bar chart display. |
| `requirements.txt` | List of Python dependencies needed to run the project. |

---

## ⚙️ Setup and How to Run Locally

### 1. Open Terminal in the Project Directory
```bash
cd "e:\Users\sunil\Desktop\PROJECTS\ML APRIORI"
```

### 2. Activate the Virtual Environment
If you are using the included `venvML` environment:

- **Windows (PowerShell):**
  ```powershell
  .\venvML\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```cmd
  venvML\Scripts\activate.bat
  ```
- **Or create a fresh environment:**
  ```bash
  python -m venv venv
  # Windows
  .\venv\Scripts\activate
  # Mac/Linux
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### 3. Start the Flask App
```bash
python app.py
```

### 4. View in Browser
Open your web browser and go to:
```
http://127.0.0.1:5000
```
Type any grocery item (such as `whole milk`, `yogurt`, `soda`, or `rolls/buns`) and click **Get Suggestions**.

---

## 🔄 Re-running the Apriori Model (Optional)

If you ever want to change thresholds (e.g., minimum support or lift) or update the dataset, run:
```bash
python "apriori code.py"
```
This will recreate `Dataset14-Grocery-MarketBasket-Analysis.pkl`, which `app.py` will then load.

---

## 🔌 Application Routes

The Flask app (`app.py`) provides the following endpoints:

| Route | Method | Description |
| :--- | :---: | :--- |
| `/` | `GET` | Renders `templates/index.html` (the user interface). |
| `/recommend?item=<name>` | `GET` | Returns a JSON response with the input item and top suggested products. |
| `/reco_bar_chart?item=<name>` | `GET` | Generates and sends a PNG image of the frequency comparison bar chart. |

---

## 🛠️ Built With

- **Python 3**
- **Pandas** — Data manipulation and cross-tabulation
- **Mlxtend** — Apriori algorithm and association rule mining
- **Flask** — Local web server and API routing
- **Matplotlib** — Generating the horizontal bar chart
- **HTML** — Frontend user interface
