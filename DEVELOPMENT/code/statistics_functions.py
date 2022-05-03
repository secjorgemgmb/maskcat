import pandas as pd
import json

df = pd.DataFrame()

with open('results/estadisticas_historico.json') as json_file:
    data = json.load(json_file)

df = df.from_dict(data).transpose()
print(df)

for index, row in df.iterrows():
    df.at[index, "Puntuacion"] = row["Puntuacion"][0]

print(df)

media = df["Puntuacion"].mean()
max = df["Puntuacion"].max()
min = df["Puntuacion"].min()
desv_est = df["Puntuacion"].std()
moda = df["Puntuacion"].mode()[0]
mediana = df["Puntuacion"].median()

df.to_csv("prueba.csv", index=False)
