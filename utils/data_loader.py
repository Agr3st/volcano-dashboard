import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data():
    eruptions_1 = pd.read_csv("data/raw_data.csv", usecols=[
        "Volcano Name", "Eruption Category", "VEI", "Start Year", "End Year", "Latitude", "Longitude", "Evidence Method (dating)"
    ], skiprows=1)

    eruptions_1[["Evidence Type", "Evidence Method"]] = eruptions_1["Evidence Method (dating)"].str.split(": ", expand=True)
    eruptions_1.drop(columns="Evidence Method (dating)", inplace=True)
    eruptions_1.fillna(value={"Evidence Type": "Uncertain", "Evidence Method": "Unspecified"}, inplace=True)
    eruptions_1 = eruptions_1[eruptions_1["Eruption Category"] != "Discredited Eruption"]

    eruptions_2 = pd.read_csv("data/volcanoes_name_country.csv", sep=";", usecols=["Volcano Name", "Country"], encoding="utf-8-sig")

    eruptions_3 = pd.read_csv("data/volcano_activity.csv", usecols=["Volcano", "Eruption Start Date", "Last Known Activity", "WVAR"])
    eruptions_3 = eruptions_3.rename(columns={"Volcano": "Volcano Name"})

    eruptions_3 = eruptions_3.merge(
        eruptions_1[["Volcano Name", "Latitude", "Longitude"]].drop_duplicates(),
        on="Volcano Name", how="left"
    ).merge(eruptions_2, on="Volcano Name", how="left")

    eruptions_3["WVAR"] = eruptions_3["WVAR"].fillna("No")

    eruptions_data = eruptions_1.merge(eruptions_2, on="Volcano Name", how="outer")
    eruptions_data.dropna(subset="VEI", inplace=True)
    eruptions_data["VEI"] = eruptions_data["VEI"].astype(int)
    eruptions_data["Start Year"] = eruptions_data["Start Year"].astype(int)
    eruptions_data["End Year"] = eruptions_data["End Year"].fillna("unknown")

    def convert_end_year(val):
        try:
            if isinstance(val, float) and not np.isnan(val):
                return int(val)
            elif isinstance(val, str) and val != "unknown":
                return int(float(val))
            else:
                return val
        except (Exception, ):
            return val

    eruptions_data["End Year"] = eruptions_data["End Year"].apply(convert_end_year)
    eruptions_data["Years of activity + VEI"] = "Years: " + eruptions_data["Start Year"].astype(str) + "-" + eruptions_data["End Year"].astype(str) + "; VEI: " + eruptions_data["VEI"].astype(str)

    return eruptions_data, eruptions_3
