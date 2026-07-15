import pandas as pd 
import os 

class DataLoader:
    def __init__(self, data_dir = "data"):
        self.data_dir = data_dir
    
    def load_coordinates(self):
        path = os.path.join(self.data_dir, "coordinates.csv")
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            ## tmp
            return pd.DataFrame({
                'Country': ['Germany', 'Czechia', 'Slovakia', 'Austria', 'France', 'Poland'],
                'latitude': [51.165691, 49.817492, 48.669026, 47.516231, 46.227638, 51.9194],
                'longitude': [10.451526, 15.472962, 19.699024, 14.550072, 2.213749, 19.1451]
            })
        
    def load_population(self):
        path = os.path.join(self.data_dir, "population.csv")
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            ## tmp
            return pd.DataFrame({
                'Country': ['Germany', 'Czechia', 'Slovakia', 'Austria', 'France', 'Poland'],
                'Population': [83000000, 10700000, 5400000, 8900000, 6700000, 38000000]
            })
        
    def load_refugees(self):
        path = os.path.join(self.data_dir, "temporary_protection.csv")
        return pd.read_csv(path)
    
    def get_distinations_data(self):
        coords = self.load_coordinates()
        pop = self.load_population()

        destinations_df = pd.merge(coords, pop, on='Country', how='inner')
        destinations_df = destinations_df.dropna(subset=['latitude', 'longitude', 'Population'])

        return destinations_df