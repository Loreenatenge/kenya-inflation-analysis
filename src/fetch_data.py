import pandas as pd
import requests

def get_world_bank_data(indicator, country="KE", start=1980, end=2024):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start}:{end}&format=json&per_page=100"
    response = requests.get(url)
    data = response.json()
    records = []
    for entry in data[1]:
        records.append({
            "year": int(entry["date"]),
            "value": entry["value"]
        })
    df = pd.DataFrame(records)
    df = df.sort_values("year").reset_index(drop=True)
    return df

exchange = get_world_bank_data("PA.NUS.FCRF")
exchange = exchange.rename(columns={"value": "exchange_rate"})

gdp = get_world_bank_data("NY.GDP.MKTP.KD.ZG")
gdp = gdp.rename(columns={"value": "gdp_growth"})

food = get_world_bank_data("AG.PRD.FOOD.XD")
food = food.rename(columns={"value": "food_index"})
df = exchange.merge(gdp, on="year").merge(food, on="year")

print(df.head(10))
print(df.isnull().sum())

df.to_csv("data/cleaned/extra_data.csv", index=False)
print("done")
