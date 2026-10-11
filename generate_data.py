import pandas as pd
import numpy as np

# Set up approximate coordinates for Vellore city
np.random.seed(42)
num_wards = 60

data = {
    "Ward": [f"Ward {i}" for i in range(1, num_wards + 1)],
    "Lat": np.random.uniform(12.88, 12.95, num_wards),
    "Lon": np.random.uniform(79.10, 79.17, num_wards),
    "Population": np.random.randint(5000, 15000, num_wards),
    "Supply_Days_Per_Week": np.random.randint(1, 4, num_wards),
    "Pipe_Age_Years": np.random.randint(10, 50, num_wards),
    "Septic_Reliance_Pct": np.random.uniform(0.3, 0.9, num_wards)
}
df = pd.DataFrame(data)

# Transparent Risk Formula
df["Pressure_Loss_Prob"] = 1 - (df["Supply_Days_Per_Week"] / 7)
df["Risk_Score"] = df["Pressure_Loss_Prob"] * df["Septic_Reliance_Pct"] * (df["Population"] / 15000)

# Categorize for the triage map
df["Risk_Level"] = pd.cut(df["Risk_Score"], bins=[0, 0.3, 0.6, 1.0], labels=["Green", "Amber", "Red"])

df.to_csv("vellore_wards.csv", index=False)
print("Synthetic dataset 'vellore_wards.csv' generated!")