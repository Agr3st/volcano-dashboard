import requests
from bs4 import BeautifulSoup
import csv

url = 'https://volcano.si.edu/gvp_currenteruptions.cfm'

# pobranie strony
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# szukanie tabeli z danymi
table = soup.find('div', class_='TableSearchResults').find('table')

# lista nagłówków
headers = ['Volcano', 'Country', 'Eruption Start Date', 'Last Known Activity']

# lista do przechowywania danych
rows = []

# iteracja przez wyszstkie wiersze tabeli
for tr in table.find_all('tr'):
    # pominięcie nagłówka
    if tr.find('th'):
        continue
    # pobranie wszystkich komórek
    tds = tr.find_all('td')
    if len(tds) >= 4:
        volcano = tds[0].get_text(strip=True)
        country = tds[1].get_text(strip=True)
        eruption_start = tds[2].get_text(strip=True)
        last_activity = tds[3].get_text(strip=True)
        rows.append([volcano, country, eruption_start, last_activity])

# Zapisz do CSV
with open('../data/volcano_activity.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

