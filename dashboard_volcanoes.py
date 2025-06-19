# dashboard_volcanoes.py
import streamlit as st
from utils.data_loader import load_data
from utils.filters import *
from utils.map_utils import generate_map
import plotly.express as px
from streamlit_folium import st_folium

st.set_page_config(page_title="🌋 Dashboard Wulkanów", layout="wide")

# Wczytywanie danych
eruptions, active_eruptions = load_data()

# Sidebar
st.sidebar.title("🔍 Filtry")

# wybór coutry
all_countries = sorted(eruptions["Country"].dropna().unique())
selected_country = st.sidebar.selectbox("Wybierz kraj", ["Wszystkie"] + all_countries)

# wybór trybu filtracji i wybranie wartości VEI
vei_filter_mode = st.sidebar.radio("Tryb filtrowania VEI:", ["Zakres", "Konkretna wartość"])
if vei_filter_mode == "Zakres":
    vei_range = st.sidebar.slider("Wybierz zakres wartości VEI", min_value=0, max_value=7, value=(5, 6))
    selected_vei = None  # nie używamy
else:
    selected_vei = st.sidebar.selectbox("Wybierz konkretną wartość VEI", list(range(0, 8)), index=7)
    vei_range = None  # nie używamy

# wybór czy tylko trwające erupcje
only_ongoing = st.sidebar.checkbox("Tylko trwające erupcje", value=False)

# Filtrowanie
# po krajach
eruptions = filter_by_country(eruptions, selected_country)

# po wartościach VEI
if vei_filter_mode == "Zakres" and vei_range:
    eruptions = filter_by_vei_range(eruptions, vei_range)
elif vei_filter_mode == "Konkretna wartość" and selected_vei is not None:
    eruptions = filter_by_vei(eruptions, selected_vei)

# aktywne erupcje - po wszystkich wartościach
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
vei_chart = px.histogram(eruptions, x="Country", color="VEI", barmode="group", title="Liczba wszystkich dotychczasowych erupcji wg kraju i VEI")
st.plotly_chart(vei_chart, use_container_width=True)

# Ciekawostka
st.subheader("🧠 Ciekawostka")
if not eruptions.empty:
    top_vei = eruptions.loc[eruptions["VEI"].idxmax()]
    st.markdown(f"**Najbardziej eksplozywna erupcja:** {top_vei['Volcano Name']} ({top_vei['VEI']}) – {top_vei['Country']}")
else:
    st.info("Brak danych dla wybranych filtrów.")
