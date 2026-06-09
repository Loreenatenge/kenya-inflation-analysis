import pandas as pd

df = pd.read_csv("data/raw/wb_data.csv", skipfooter=5, engine="python")


df = df.drop(columns=["Country Name", "Country Code", "Series Code"])

df.columns = [col.split(" ")[0] if col.startswith("19") or col.startswith("20") else col for col in df.columns]


df = df.melt(id_vars=["Series Name"], var_name="year", value_name="value")


df = df.pivot(index="year", columns="Series Name", values="value").reset_index()
df.columns.name = None
df = df.rename(columns={
    "year": "year",
    "Broad money (% of GDP)": "broad_money",
    "Inflation, consumer prices (annual %)": "inflation"
})
df["year"] = df["year"].astype(int)

print(df.isnull().sum())


df.to_csv("data/cleaned/kenya_data.csv", index=False)

print("done")
print(df.head())

