import matplotlib.pyplot as plt
import pandas as pd

pm25 = pd.read_csv("data/processed/zonal_pm25_winter.csv")
ndvi = pd.read_csv("data/processed/zonal_ndvi_winter.csv")

# Rename for clarity
pm25 = pm25.rename(columns={"pm25": "pm25_winter"})

# Merge on zone + year
merged = pm25.merge(
    ndvi,
    on=["zone", "year"],
    how="inner"
)

print("Merged rows:", len(merged))
print(merged.head())

merged.to_csv("data/processed/zone_winter_pm25_ndvi.csv", index=False)

pearson = merged["pm25_winter"].corr(merged["ndvi_winter"], method="pearson")
spearman = merged["pm25_winter"].corr(merged["ndvi_winter"], method="spearman")

print(f"Pearson correlation : {pearson:.3f}")
print(f"Spearman correlation: {spearman:.3f}")


plt.figure(figsize=(6, 5))
plt.scatter(merged["ndvi_winter"], merged["pm25_winter"])
plt.xlabel("Winter NDVI")
plt.ylabel("Winter PM2.5 (µg/m³)")
plt.title("NDVI vs PM2.5 (Delhi Zones)")
plt.grid(True)
plt.tight_layout()
plt.show()
