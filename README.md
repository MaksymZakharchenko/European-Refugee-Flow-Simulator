# 🌍 European Refugee Flow Analytics Platform

An advanced end-to-end Machine Learning and simulation platform designed to model, predict, and analyze cross-border population displacement during hypothetical humanitarian crises in Europe. 

Developed as a robust portfolio project demonstrating production-ready data pipelines, heuristic vs. machine learning model comparisons, validation metrics, and Explainable AI (XAI).

---

## 🚀 Key Features

* **Interactive Crisis Scenario Simulation:** Configure origin countries, affected population percentages, and crisis duration dynamically via a clean Streamlit interface.
* **Dual Modeling Approach:**
  * **Gravity Migration Model (Heuristic):** Built on demographic gravity principles, utilizing calibrated parameters ($\beta$ and $\gamma$) inspired by historical refugee movements.
  * **Random Forest Regressor (Machine Learning):** Supervised machine learning model trained to predict migration distribution based on multiple demographic and geographic features.
* **Model Validation Metrics:** Rigorous statistical evaluation tracking model accuracy via **MAE** (Mean Absolute Error), **RMSE** (Root Mean Squared Error), and **$R^2$ Score** (Coefficient of Determination).
* **Explainable AI (XAI):** Integrated **SHAP (SHapley Additive exPlanations)** analysis for the Machine Learning model to ensure transparency and explain feature importance (crucial for model compliance and auditing).
* **Animated Geographical Visualizations:** Interactive choropleth maps built with Plotly, featuring a timeline animation of population flows day-by-day.

---

## 🛠️ Tech Stack

* **Language:** Python[cite: 1]
* **Web Framework:** Streamlit[cite: 1]
* **Data Processing & ML:** Pandas, NumPy, Scikit-Learn
* **Visualization:** Plotly, Matplotlib, Seaborn[cite: 1]
* **Explainability:** SHAP
* **Version Control:** Git & GitHub[cite: 1]

---

## 📁 Project Structure

```text
European-Refugee-Flow-Simulator/
│
├── dashboard/
│   └── app.py              # Main Streamlit web application UI & logic
├── models/
│   └── gravity_model.py    # Core mathematical/heuristic migration model
├── utils/
│   └── loader.py           # Data ingestion, cleaning, and ETL pipeline
├── data/
│   └── coordinates.csv     # Geographic and demographic dataset
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation

⚙️ Installation & Running Locally
Clone the repository:
Bash
git clone [https://github.com/YOUR_USERNAME/European-Refugee-Flow-Simulator.git](https://github.com/YOUR_USERNAME/European-Refugee-Flow-Simulator.git)
cd European-Refugee-Flow-Simulator
Create and activate a virtual environment:
Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install dependencies:
Bash
pip install -r requirements.txt
Run the Streamlit application:
Bash
streamlit run dashboard/app.py
📊 Analytics & Validation Methodology
In financial and risk analytics, models must not only perform well but also be fully transparent and validated. This platform incorporates standard statistical validation frameworks to test predictions against baseline historical datasets, minimizing black-box uncertainty through SHAP value attribution.

---

### Jak wrzucić projekt na GitHub, żeby strona była publiczna? (Krok po kroku)

1. **Stwórz publiczne repozytorium na GitHubie:**
   * Wejdź na [github.com](https://github.com/) i zaloguj się.
   * W prawym górnym rogu kliknij ikonę **`+`** -> **`New repository`**.
   * Wpisz nazwę (np. `European-Refugee-Flow-Simulator`).
   * Zaznacz opcję **Public** (dzięki temu repozytorium i kod będą widoczne dla rekruterów).
   * **Nie zaznaczaj** opcji "Add a README file" (ponieważ stworzyliśmy go przed chwilą u siebie).
   * Kliknij **`Create repository`**.

2. **Wgraj swój kod przez terminal (w folderze głównym Twojego projektu):**
   Otwórz terminal w folderze projektu i wpisz kolejno te komendy (podmień `TWOJ_LOGIN_GITHUB` na swój faktyczny login):

   ```bash
   git init
   git add .
   git commit -m "Initial commit: Add refugee flow simulator with ML, SHAP and Streamlit"
   git branch -M main
   git remote add origin https://github.com/TWOJ_LOGIN_GITHUB/European-Refugee-Flow-Simulator.git
   git push -u origin main