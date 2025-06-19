def filter_by_country(df, country):
    if country == "Wszystkie":
        return df
    return df[df["Country"] == country]

def filter_by_vei(df, min_vei):
    return df[df["VEI"] >= min_vei]

def filter_by_wvar(df, only_wvar):
    if only_wvar:
        return df[df["WVAR"] == "Yes"]
    return df
