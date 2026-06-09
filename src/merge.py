import pandas as pd

wb = pd.read_csv("data/cleaned/kenya_data.csv")
extra = pd.read_csv("data/cleaned/extra_data.csv")


df = wb.merge(extra, on="year")

df["food_index"] = df["food_index"].interpolate()
print(df.shape)
print(df.isnull().sum())
print(df.head(10))


df.to_csv("data/cleaned/kenya_final.csv", index=False)
print("saved")
