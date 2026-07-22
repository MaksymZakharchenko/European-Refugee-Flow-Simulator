import pandas as pd
import os

class DataLoader:
    def __init__(self, data_dir="data/raw"):
        self.data_dir = data_dir if os.path.exists(data_dir) else "data"

    def _normalize_country_column(self, df):
        if 'geo' in df.columns:
            df = df.rename(columns={'geo': 'Country'})
        elif 'country' in df.columns:
            df = df.rename(columns={'country': 'Country'})
            
        if 'Country' in df.columns:
            df['Country'] = df['Country'].replace({'Czechia': 'Czech Republic'})
            df['Country'] = df['Country'].astype(str).str.strip()
            
            eurostat_map = {
                'PL': 'Poland', 'DE': 'Germany', 'CZ': 'Czechia', 'SK': 'Slovakia',
                'AT': 'Austria', 'FR': 'France', 'IT': 'Italy', 'RO': 'Romania',
                'ES': 'Spain', 'HU': 'Hungary', 'BG': 'Bulgaria', 'NL': 'Netherlands'
            }
 
            df['Country'] = df['Country'].apply(lambda x: eurostat_map.get(x, x))
            
        return df

    def load_coordinates(self):
        path = os.path.join(self.data_dir, "coordinates.csv")
        coords = pd.read_csv(path, sep=';') 
        coords = self._normalize_country_column(coords)
        return coords

    def load_population(self):
        path = os.path.join(self.data_dir, "population.csv")
        pop_df = pd.read_csv(path, sep=';' if ';' in open(path).readline() else ',')
        
        pop_df = self._normalize_country_column(pop_df)
            
        if 'OBS_VALUE' in pop_df.columns:
            pop_df = pop_df.rename(columns={'OBS_VALUE': 'Population'})
            
        if 'TIME_PERIOD' in pop_df.columns:
            latest_year = pop_df['TIME_PERIOD'].max()
            pop_df = pop_df[pop_df['TIME_PERIOD'] == latest_year]
            
        pop_df = pop_df.dropna(subset=['Country', 'Population'])
        return pop_df[['Country', 'Population']]

    def load_refugees(self):
        path = os.path.join(self.data_dir, "temporary_protection.csv")
        ref_df = pd.read_csv(path, sep=';' if ';' in open(path).readline() else ',')
        return self._normalize_country_column(ref_df)

    def get_destinations_data(self):
        coords = self.load_coordinates()
        pop = self.load_population()

        destinations_df = pd.merge(coords, pop, on='Country', how='inner')
        return destinations_df

    def get_ukraine_data(self):
        refugees_df = self.load_refugees()
        
        if 'OBS_VALUE' in refugees_df.columns:
            refugees_df = refugees_df.dropna(subset=['Country', 'OBS_VALUE'])
            actual_flows = refugees_df.groupby('Country')['OBS_VALUE'].max().reset_index()
            actual_flows.rename(columns={'OBS_VALUE': 'actual_refugees'}, inplace=True)
        else:
            ref_col = [c for c in refugees_df.columns if c != 'Country'][0]
            refugees_df = refugees_df.dropna(subset=['Country', ref_col])
            actual_flows = refugees_df.groupby('Country')[ref_col].max().reset_index()
            actual_flows.rename(columns={ref_col: 'actual_refugees'}, inplace=True)

        destinations = self.get_destinations_data()
        training_df = pd.merge(destinations, actual_flows, on='Country', how='inner')
        return training_df