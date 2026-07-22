import sys 
import os 
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.gravity_model import GravityMigrationModel
from utils.loader import DataLoader

def run_training():
    print("⏳ Ładowanie i czyszczenie danych z Eurostatu...")
    loader = DataLoader()
    training_df = loader.get_ukraine_data()

    if training_df.empty:
        print("❌ Błąd: Nie udało się złączyć danych treningowych. Sprawdź pliki CSV.")
        return
    
    print(f"✅ Znaleziono historyczne dane dla {len(training_df)} państw.")

    ukraine_lat, ukraine_lon = 50.4501, 30.5234

    total_ukraine_refugees = training_df['actual_refugees'].sum()
    print(f"🌍 Całkowita liczba uchodźców w zbiorze: {total_ukraine_refugees:,.0f}") 

    model = GravityMigrationModel(beta=1.0, gamma=2.0)

    print("\n🧠 Rozpoczęcie procesu kalibracji (Machine Learning)...")
    best_beta, best_gamma = model.fit(
        origin_lat=ukraine_lat,
        origin_lon=ukraine_lon,
        total_displaced=total_ukraine_refugees,
        destinations_df=training_df,
        actual_refugees_col='actual_refugees'
    )

    print(f"\n🎉 Trening zakończony sukcesem!")
    print(f"Wyliczona Waga Populacji (Beta): {best_beta:.4f}")
    print(f"Wyliczona Kara za Dystans (Gamma): {best_gamma:.4f}")

    predictions = model.predict_flows(ukraine_lat, ukraine_lon, total_ukraine_refugees, training_df)
    final_df = pd.merge (predictions, training_df[['Country', 'actual_refugees']], on="Country")

    print("\n📊 Zestawienie wyników (Predykcja vs Rzeczywistość):")
    print(predictions[['Country', 'actual_refugees', 'predicted_refugees']].head(30).to_string(index=False))

if __name__ == "__main__":
    run_training()