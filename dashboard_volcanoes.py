# dashboard_volcanoes.py
import streamlit as st
from utils.data_loader import load_data
from utils.filters import filter_by_country, filter_by_vei, filter_by_wvar
from utils.map_utils import generate_map
import plotly.express as px
from streamlit_folium import st_folium

st.set_page_config(page_title="🌋 Dashboard Wulkanów", layout="wide")

# Wczytywanie danych
eruptions, active_eruptions = load_data()

# Sidebar
st.sidebar.title("🔍 Filtry")
all_countries = sorted(eruptions["Country"].dropna().unique())
selected_country = st.sidebar.selectbox("Wybierz kraj", ["Wszystkie"] + all_countries)
selected_vei = st.sidebar.slider("Minimalne VEI (indeks eksplozywności)", min_value=0, max_value=8, value=0)
only_ongoing = st.sidebar.checkbox("Tylko trwające erupcje", value=False)

# Filtrowanie
eruptions = filter_by_country(eruptions, selected_country)
eruptions = filter_by_vei(eruptions, selected_vei)

active_eruptions = filter_by_country(active_eruptions, selected_country)
active_eruptions = filter_by_wvar(active_eruptions, only_ongoing)

# Mapa
st.title("🌍 Interaktywna Mapa Wulkanów")

if len(eruptions) + len(active_eruptions) > 700:
    st.warning("Zbyt wiele punktów do wyświetlenia. Zawęż filtry, aby poprawić wydajność.")
else:
    m = generate_map(eruptions, active_eruptions, only_ongoing)
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
