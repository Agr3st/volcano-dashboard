# 🌋 Dashboard Wulkanów

Interaktywny dashboard prezentujący aktywność wulkaniczną na świecie.

Aplikacja: https://volcano-dashboard.streamlit.app/

Źródło danych: https://volcano.si.edu/

---

## Funkcje

- Interaktywna mapa wulkanów z rozróżnieniem erupcji historycznych, trwających oraz uwzględnionych w raporcie WVAR
- Filtrowanie po kraju, indeksie eksplozywności (VEI) oraz statusie erupcji
- Wizualizacja VEI wg krajów
- Automatyczny skrypt do pobierania najnowszych danych o aktywnych erupcjach

---

## Struktura projektu

```

├── dashboard_volcanoes.py       # Główny plik aplikacji Streamlit
├── scraper/
│   └── scrape_current_eruptions.py  # Skrypt do pobierania danych o erupcjach
├── utils/
│   ├── data_loader.py           # Funkcje do wczytywania i przetwarzania danych
│   ├── filters.py               # Funkcje filtrujące dane
│   └── map_utils.py             # Funkcje do generowania mapy
├── data/
│   ├── raw_data.csv             # Dane historyczne
│   ├── volcanoes_name_country.csv
│   └── volcano_activity.csv     # Dane o aktywnej erupcji (aktualizowane scraperem)
├── .github/workflows/
│   └── update_data.yml       # Workflow GitHub Actions aktualizujący dane
└── README.md                    # Ten plik

```

---

## Jak uruchomić lokalnie

1. Sklonuj repozytorium:
```

git clone https://github.com/TWOJE_UZYTKOWNIK/volcano-dashboard.git
cd volcano-dashboard

```

2. Stwórz środowisko virtualne (zalecane conda lub venv) i zainstaluj wymagania:
```

pip install -r requirements.txt

```

3. Uruchom aplikację Streamlit:
```

streamlit run dashboard_volcanoes.py

```

---

## Automatyczna aktualizacja danych

Projekt zawiera GitHub Actions, który co określony czas uruchamia scraper `scrape_current_eruptions.py`, aktualizuje plik `data/volcano_activity.csv` i robi commit do repozytorium (jeśli w pliku zajdą zmiany).



Jeśli chcesz, mogę pomóc też z generowaniem pliku `requirements.txt` albo innymi dokumentami.
Chcesz?
