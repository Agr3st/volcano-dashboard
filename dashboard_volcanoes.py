import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px


# dashboard_volcanoes.py


# Wczytanie danych
@st.cache_data
def load_data():
    df = pd.read_csv("volcanoes.csv", sep=';', skiprows=1)  
    # Zamiana przecinków na kropki w liczbach zmiennoprzecinkowych
    df["Latitude"] = df["Latitude"].str.replace(",", ".").astype(float)
    df["Longitude"] = df["Longitude"].str.replace(",", ".").astype(float)
    # Konwersja daty
    df["Last Known Eruption"] = pd.to_datetime(df["Last Known Eruption"], errors='coerce')
    return df

df = load_data()
# Sidebar: filtry
st.sidebar.title("🔍 Filtry")
country = st.sidebar.selectbox("Wybierz kraj", options=["Wszystkie"] + sorted(df["Country"].unique().tolist()))
volcano_type = st.sidebar.selectbox("Typ wulkanu", options=["Wszystkie"] + sorted(df["Primary Volcano Type"].dropna().unique()))

# Filtrowanie
if country != "Wszystkie":
    df = df[df["Country"] == country]
if volcano_type != "Wszystkie":
    df = df[df["Primary Volcano Type"] == volcano_type]

# Mapa
st.title("🌋 Interaktywna Mapa Wulkanów")
m = folium.Map(location=[0, 0], zoom_start=2)

for _, row in df.iterrows():
    color = 'gray' if pd.notna(row["Last Known Eruption"]) and row["Last Known Eruption"].year < 2023 else 'red'
    popup_html = f"""
    <b>{row['Volcano Name']}</b><br>
    <a href="https://en.wikipedia.org/wiki/{row['Volcano Name'].replace(' ', '_')}" target="_blank">Wikipedia</a><br>
    Kraj: {row['Country']}<br>
    Wysokość: {row['Elevation (m)']} m
    """
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=5,
        color=color,
        fill=True,
        fill_opacity=0.7,
        popup=popup_html
    ).add_to(m)

st_folium(m, width=700)

# Wykresy statystyczne
st.header("📊 Statystyki Historyczne")
fig = px.histogram(df, x="Country", title="Liczba wulkanów wg kraju", color="Country")
st.plotly_chart(fig, use_container_width=True)

# Ciekawostki
st.subheader("🧠 Ciekawostka")
max_height = df.loc[df["Elevation (m)"].idxmax()]
st.markdown(f"**Najwyższy wulkan:** {max_height['Volcano Name']} w {max_height['Country']} ({max_height['Elevation (m)']} m)")

