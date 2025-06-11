import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import plotly.express as px

st.set_page_config(page_title="🌋 Dashboard Wulkanów", layout="wide")

# Wczytywanie danych
@st.cache_data
def load_data():
    eruptions_1 = pd.read_csv("raw_data.csv", usecols=[
        "Volcano Name", "Eruption Category", "VEI", "Start Year", "End Year", "Latitude", "Longitude", "Evidence Method (dating)"
    ], skiprows=1)

    eruptions_1[["Evidence Type", "Evidence Method"]] = eruptions_1["Evidence Method (dating)"].str.split(": ", expand=True)
    eruptions_1.drop(columns="Evidence Method (dating)", inplace=True)
    eruptions_1.fillna(value={"Evidence Type": "Uncertain", "Evidence Method": "Unspecified"}, inplace=True)
    eruptions_1 = eruptions_1[eruptions_1["Eruption Category"] != "Discredited Eruption"]

    eruptions_2 = pd.read_csv("volcanoes_name_country.csv", sep=";", usecols=["Volcano Name", "Country"], encoding="utf-8-sig")

    eruptions_3 = pd.read_csv("volcano_activity.csv", usecols=["Volcano", "Start Date", "Last Known Activity", "Ongoing Eruption"])
    eruptions_3 = eruptions_3.rename(columns={"Volcano": "Volcano Name"})

    # Łączenie współrzędnych
    eruptions_3 = eruptions_3.merge(
        eruptions_1[["Volcano Name", "Latitude", "Longitude"]].drop_duplicates(),
        on="Volcano Name",
        how="left"
    )
    eruptions_3 = eruptions_3.merge(eruptions_2, on="Volcano Name", how="left")
    eruptions_3["Ongoing Eruption"] = eruptions_3["Ongoing Eruption"].fillna("No")

    # Główna tabela historyczna
    eruptions = eruptions_1.merge(eruptions_2, on="Volcano Name", how="outer")
    eruptions.dropna(subset="VEI", inplace=True)
    eruptions["VEI"] = eruptions["VEI"].astype(int)
    eruptions["Start Year"] = eruptions["Start Year"].astype(int)
    eruptions["End Year"] = eruptions["End Year"].fillna("unknown")

    def convert_end_year(val):
        try:
            if isinstance(val, float) and not np.isnan(val):
                return int(val)
            elif isinstance(val, str) and val != "unknown":
                return int(float(val))
            else:
                return val
        except:
            return val

    eruptions["End Year"] = eruptions["End Year"].apply(convert_end_year)
    eruptions["Years of activity + VEI"] = "Years: " + eruptions["Start Year"].astype(str) + "-" + eruptions["End Year"].astype(str) + "; VEI: " + eruptions["VEI"].astype(str)

    return eruptions, eruptions_3

eruptions, active_eruptions = load_data()

# Sidebar
st.sidebar.title("🔍 Filtry")
all_countries = sorted(eruptions["Country"].dropna().unique())
selected_country = st.sidebar.selectbox("Wybierz kraj", ["Wszystkie"] + all_countries)
selected_vei = st.sidebar.slider("Minimalne VEI (indeks eksplozywności)", min_value=0, max_value=8, value=0)
only_ongoing = st.sidebar.checkbox("Tylko trwające erupcje", value=False)

# Filtrowanie
if selected_country != "Wszystkie":
    eruptions = eruptions[eruptions["Country"] == selected_country]
    active_eruptions = active_eruptions[active_eruptions["Country"] == selected_country]

eruptions = eruptions[eruptions["VEI"] >= selected_vei]

if only_ongoing:
    active_eruptions = active_eruptions[active_eruptions["Ongoing Eruption"] == "Yes"]

# Mapa
st.title("🌍 Interaktywna Mapa Wulkanów")

# Ostrzeżenie przy dużej liczbie punktów
if len(eruptions) + len(active_eruptions) > 700:
    st.warning("Zbyt wiele punktów do wyświetlenia. Zawęź filtry, aby poprawić wydajność.")
else:
    m = folium.Map(location=[0, 0], zoom_start=2)
    cluster = MarkerCluster().add_to(m)

    # Warstwa 1 – erupcje historyczne
    # Warstwa 1 – erupcje historyczne (tylko jeśli nie zaznaczono "tylko trwające")
    if not only_ongoing:
        for _, row in eruptions.iterrows():
            if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
                folium.CircleMarker(
                    location=[row["Latitude"], row["Longitude"]],
                    radius=4,
                    color='gray',
                    fill=True,
                    fill_opacity=0.5,
                    popup=folium.Popup(
                        f"<b>{row['Volcano Name']}</b><br>{row['Years of activity + VEI']}",
                        max_width=300
                    )
                ).add_to(m)


    # Warstwa 2 – aktywne wulkany
    for _, row in active_eruptions.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            folium.CircleMarker(
                location=[row["Latitude"], row["Longitude"]],
                radius=6,
                color='red',
                fill=True,
                fill_opacity=0.8,
                popup=folium.Popup(
                    f"<b>{row['Volcano Name']}</b><br>"
                    f"Start Date: {row['Start Date']}<br>"
                    f"Last Known Activity: {row['Last Known Activity']}<br>"
                    f"Ongoing Eruption: {row['Ongoing Eruption']}",
                    max_width=300
                )
            ).add_to(cluster)

    # Wyświetlenie mapy
    st_folium(m, width=1000, height=600)

# Wykres
st.header("📊 VEI wg kraju")
vei_chart = px.histogram(eruptions, x="Country", color="VEI", barmode="group", title="Liczba erupcji wg kraju i VEI")
st.plotly_chart(vei_chart, use_container_width=True)

# Ciekawostka
st.subheader("🧠 Ciekawostka")
if not eruptions.empty:
    top_vei = eruptions.loc[eruptions["VEI"].idxmax()]
    st.markdown(f"**Najbardziej eksplozywna erupcja:** {top_vei['Volcano Name']} ({top_vei['VEI']}) – {top_vei['Country']}")
else:
    st.info("Brak danych dla wybranych filtrów.")
