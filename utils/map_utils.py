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
                    popup=folium.Popup(
                        f"<b>{row['Volcano Name']}</b><br>{row['Years of activity + VEI']}",
                        max_width=800
                    )
                ).add_to(m)

    for _, row in active_eruptions.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            folium.CircleMarker(
                location=(row["Latitude"], row["Longitude"]),
                radius=6,
                color='darkred' if row["WVAR"] == "Yes" else 'orange',
                fill=True,
                fill_opacity=0.8,
                popup=folium.Popup(
                    f"<b>{row['Volcano Name']}</b><br>"
                    f"<b>Eruption start Date</b>: {row['Eruption Start Date']}<br>"
                    f"<b>Last Known Activity</b>: {row['Last Known Activity']}<br>"
                    f"<b>WVAR</b>: {row['WVAR']}",
                    max_width=800
                )
            ).add_to(cluster)

    return m
