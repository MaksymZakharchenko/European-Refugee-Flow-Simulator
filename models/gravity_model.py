import pandas as pd
import numpy as np
from utils.preprocessing import calculate_haversine_distance

class GravityMigrationModel:
    def __init__(self, beta = 1.0, gamma = 2.0):
        self.beta = beta
        self.gamma = gamma
    
    def predict_flows(self, origin_lat, origin_lon, total_displaced, destinations_df):
        df = destinations_df.copy()

        df['distance_km'] = calculate_haversine_distance(
            origin_lat,
            origin_lon,
            df['latitude'],
            df['longitude']
        )

        df = df[df['distance_km'] > 10].copy()

        df['gravity_score'] = (df['Population']**self.beta) / (df['distance_km']**self.gamma)

        total_score = df['gravity_score'].sum()
        df['share'] = df['gravity_score'] / total_score

        df['predicted_refugees'] = np.floor(df['share'] * total_displaced).astype(int)

        result_df = df.sort_values(by = 'predicted_refugees', ascending = False).reset_index(drop=True)

        return result_df[['Country','distance_km', 'predicted_refugees', 'share']]
        
    