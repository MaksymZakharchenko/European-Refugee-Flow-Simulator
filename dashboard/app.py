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
        loader = DataLoader()
        destinations = loader.get_distinations_data()

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
            model = GravityMigrationModel(beta=1.0, gamma=2.0)

            results = model.predict_flows(
                origin_lat=origin_lat,
                origin_lon=origin_lon,
                total_displaced=total_displaced,
                destinations_df=destinations
            )

            st.subheader("Predicted Refugee Distribution")
            st.dataframe(
                results[['Country', 'distance_km', 'predicted_refugees', 'share']]
                .style.format({
                    'distance_km': '{:1f} km',
                    'predicted_refugees': '{:,}',
                    'share': '{:.2%}'
                }),
                use_container_width = True
            )

    else:
        st.info("Configure a scenario and press Run Simulation")