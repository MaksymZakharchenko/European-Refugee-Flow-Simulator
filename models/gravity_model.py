import pandas as pd
import numpy as np
from utils.preprocessing import calculate_haversine_distance

from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error

class GravityMigrationModel:
    def __init__(self, beta = 1.0, gamma = 2.0):
        self.beta = beta
        self.gamma = gamma
    
    def predict_flows(self, origin_lat, origin_lon, total_displaced, destinations_df):
        df = destinations_df.copy()

        neighbors = ['Poland', 'Slovakia', 'Hungary', 'Romania', 'Moldova', 'Czechia']
        df['border_bonus'] = df['Country'].apply (lambda x: 3 if x in neighbors else 1.0)
        if 'distance_km' not in df.columns:
            df['distance_km'] = calculate_haversine_distance(
                origin_lat,
                origin_lon,
                df['latitude'],
                df['longitude']
            )

        df = df[df['distance_km'] > 10].copy()
        pop_scaled = df['Population'] / 10000000
        df['gravity_score'] = ((pop_scaled**self.beta) / (df['distance_km']**self.gamma)) * df['border_bonus']

        total_score = df['gravity_score'].sum()
        df['share'] = df['gravity_score'] / total_score

        df['predicted_refugees'] = np.floor(df['share'] * total_displaced).astype(int)

        #result_df = df.sort_values(by = 'predicted_refugees', ascending = False).reset_index(drop=True)

        return df
    
    def fit(self, origin_lat, origin_lon, total_displaced, destinations_df, actual_refugees_col):
        # training on data from Ukraine
        
        def cost_function(params):
            self.beta, self.gamma = params

            if self.beta < 0 or self.gamma < 0:
                return np.inf
            
            predictions = self.predict_flows(origin_lat, origin_lon, total_displaced, destinations_df)
            #merged = pd.merge(predictions,destinations_df, on="Country")

            return mean_squared_error(predictions[actual_refugees_col], predictions['predicted_refugees'])    
       
        initial_guess = [1.0, 2.0]

        result = minimize(cost_function, initial_guess, method="Nelder-Mead")
        print (f"{result} - MINIMIZE MERGE?")
        self.beta, self.gamma = result.x
        
        return self.beta, self.gamma
    
    def predict_for_country(self, country_name, total_people, destination_df):
        coords = self.get_country_coords(country_name)
        return self.predict_flows(coords['lat'], coords['lon'], total_people, destination_df)
    