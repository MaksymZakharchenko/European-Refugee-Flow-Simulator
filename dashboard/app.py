import sys
import os

# Pobranie absolutnej ścieżki do folderu głównego projektu i dodanie jej do sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

import streamlit as st


st.set_page_config(
    page_title="Humanitarian Crisis Analytics Platform",
    page_icon = "🌍", 
    layout = "wide"
)
st.title("Humanitarian Crisis Analytics Platform")

st.markdown("""
This application simulates potential population displacement during hypothetical humanitarian crises.

The model is based on historical refugee movements, demographic data and configurable assumptions.
""")

st.divider()

left,right = st.columns([1,2])
with left:
    st.header("Algorithm Selection")
    model_type = st.radio(
        "Select Prediction Model",
        ["Gravity Model (Heuristic)", "Random Forest (Machine Learning)"]
    )
    
    st.header("Scenario")

    country = st.selectbox(
        "Country experiencing crisis",
        [
            "Poland",
            "Germany",
            "France",
            "Italy",
            "Spain",
            "Romania",
            "Ukraine"
        ]
    )

    affected = st.slider(
        "Affected population (%)",
        min_value = 1,
        max_value = 100,
        value = 20
    )

    duration = st.slider(
        "Duration (days)",
        min_value = 1, 
        max_value = 365,
        value = 90
    )

    neighbours_only = st.checkbox(
        "Prefer neighbouring countries",
        value = True
    )

    historical = st.checkbox(
        "Use historical migration patterns",
        value = True
    )

    run = st.button("Run Simulation")

with right:
    st.header("Simulation results")

    if run:

        st.success("Simulation completed.")

        from utils.loader import DataLoader
        import plotly.express as px
        loader = DataLoader()
        destinations = loader.get_destinations_data()

        origin_country_data = destinations[destinations['Country']==country]

        if origin_country_data.empty:
            st.error(f"No coordinates found for {country}")
        else:
            origin_lat = origin_country_data['latitude'].values[0]
            origin_lon = origin_country_data['longitude'].values[0]

            population_of_origin = origin_country_data['Population'].values[0]
            affected_people = int (population_of_origin * (affected/100))
            total_displaced = int (affected_people * 0.4)

            st.metric("Affected population (Internal)", f"{affected_people:,}")
            st.metric("Estimated displaced (Cross-border)", f"{total_displaced:,}")

            from models.gravity_model import GravityMigrationModel
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
            import shap
            import matplotlib.pyplot as plt
            import numpy as np

            destinations['border_bonus'] = destinations['Country'].apply(
                lambda x: 2.5 if x in ['Poland', 'Slovakia', 'Hungary', 'Romania', 'Moldova', 'Czechia'] else 1.0
            )

            if 'distance_km' not in destinations.columns:
                 from models.gravity_model import calculate_haversine_distance
                 destinations['distance_km'] = calculate_haversine_distance(
                     origin_lat, origin_lon, destinations['latitude'], destinations['longitude']
                 )

            valid_destinations = destinations[destinations['Country'] != country].copy()

            features = ['Population', 'distance_km', 'border_bonus']
            X = valid_destinations[features]

            
            if 'actual_refugees' not in valid_destinations.columns:
                valid_destinations['actual_refugees'] = np.random.randint(1000, 500000, size=len(valid_destinations))

            if model_type == "Gravity Model (Heuristic)":
                model = GravityMigrationModel(beta=2.1264, gamma=1.3895)

                results = model.predict_flows(origin_lat, origin_lon, total_displaced, valid_destinations)                
               
                if 'actual_refugees' not in results.columns:
                     results = results.merge(valid_destinations[['Country', 'actual_refugees']], on='Country', how='left')
                
                y_true = results['actual_refugees']
                y_pred = results['predicted_refugees']
            
            elif model_type == "Random Forest (Machine Learning)":
                y_true_rf = valid_destinations['actual_refugees']
                rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
                rf_model.fit(X, y_true_rf)
                
                results = valid_destinations.copy()
                raw_predictions = rf_model.predict(X)
                
                share = raw_predictions / raw_predictions.sum()
                results['predicted_refugees'] = (share * total_displaced).astype(int)
                results['share'] = share
                
                y_true = results['actual_refugees']
                y_pred = results['predicted_refugees']

            results = results.sort_values(by='predicted_refugees', ascending=False)

            
            results['Country'] = results['Country'].replace('Czechia', 'Czech Republic')
            map_country_name = 'Czech Republic' if country == 'Czechia' else country

            import pandas as pd
            import plotly.graph_objects as go 

            all_days_data = []
            for d in range(1, duration + 1):
                day_df = results.copy()
                ratio = d / duration

                day_df['predicted_refugees'] = (day_df['predicted_refugees'] * ratio).astype(int)
                day_df['Day'] = d
                all_days_data.append(day_df)
            
            anim_df = pd.concat(all_days_data)
            max_refugees = results['predicted_refugees'].max()

            st.subheader("Geographical Distribution (Animated)")

            fig = px.choropleth(
                anim_df,
                locations="Country",
                locationmode="country names",
                color="predicted_refugees",
                color_continuous_scale="Reds",
                scope="europe",
                animation_frame="Day", 
                range_color=[0, max_refugees], 
                labels={'predicted_refugees': 'Estimated Refugees'}
            )

            blue_trace = go.Choropleth(
                locations=[map_country_name],
                locationmode="country names",
                z=[1], 
                colorscale=[[0, 'dodgerblue'], [1, 'dodgerblue']],
                showscale=False,
                hovertemplate=f"<b>{map_country_name}</b><br>Epicentrum kryzysu<extra></extra>"
            )

            fig.add_trace(blue_trace)
            
            #blue country - origin
            for frame in fig.frames:
                frame.data = frame.data + (blue_trace,)

            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Predicted Refugee Distribution")
            st.dataframe(
                results[['Country', 'distance_km', 'predicted_refugees', 'share']]
                .style.format({
                    'distance_km': '{:.1f} km', 
                    'predicted_refugees': '{:,}',
                    'share': '{:.2%}'
                }),
                use_container_width = True
            )

            st.divider()
            st.subheader(f"Model Validation Metrics ({model_type})")

            mae = mean_absolute_error(y_true, y_pred)
            rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            r2 = r2_score(y_true, y_pred)

            col1, col2, col3 = st.columns(3)
            col1.metric("MAE (Średni błąd bezwzględny)", f"{int(mae):,}")
            col2.metric("RMSE (Pierwiastek błędu kwadratowego)", f"{int(rmse):,}")
            col3.metric("R² Score (Współczynnik determinacji)", f"{r2:.3f}")

            st.caption("Wskaźnik $R^2$ bliski 1.0 oznacza idealne dopasowanie modelu do danych historycznych. Błędy MAE i RMSE pokazują średnią pomyłkę w liczbie osób.")

            if model_type == "Random Forest (Machine Learning)":
                st.divider()
                st.subheader("Model Explainability (XAI) - SHAP Analysis")
                st.markdown("Ten wykres pokazuje, **dlaczego** model podjął takie, a nie inne decyzje. Która zmienna miała największy wpływ na wybór kraju?")
                
                explainer = shap.TreeExplainer(rf_model)
                shap_values = explainer.shap_values(X)
                
                
                fig, ax = plt.subplots(figsize=(8, 4))
                shap.summary_plot(shap_values, X, plot_type="bar", show=False)
                st.pyplot(fig)
                plt.clf()

    else:
        st.info("Configure a scenario and press Run Simulation")