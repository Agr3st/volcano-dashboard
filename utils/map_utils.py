import folium
import pandas as pd
from folium.plugins import MarkerCluster

def generate_map(eruptions, active_eruptions, only_ongoing):
    m = folium.Map(location=[0, 0], zoom_start=2)
    cluster = MarkerCluster().add_to(m)

    if not only_ongoing:
        for _, row in eruptions.iterrows():
            if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
                folium.CircleMarker(
                    location=(row["Latitude"], row["Longitude"]),
                    radius=4,
                    color='gray',
                    fill=True,
                    fill_opacity=0.5,
                    popup=f"<b>{row['Volcano Name']}</b><br>{row['Years of activity + VEI']}"
                ).add_to(m)

    for _, row in active_eruptions.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            folium.CircleMarker(
                location=(row["Latitude"], row["Longitude"]),
                radius=6,
                color='darkred' if row["WVAR"] == "Yes" else 'orange',
                fill=True,
                fill_opacity=0.8,
                popup=(
                    f"<b>{row['Volcano Name']}</b><br>"
                    f"Eruption start Date: {row['Eruption Start Date']}<br>"
                    f"Last Known Activity: {row['Last Known Activity']}<br>"
                    f"WVAR: {row['WVAR']}"
                )
            ).add_to(cluster)

    return m
