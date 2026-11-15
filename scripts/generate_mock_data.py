
import pandas as pd
from pathlib import Path

# Locate the project directory
project_root = Path(__file__).resolve().parents[1]

# Define mock resource data
data = {
    "resource": ["oxygen", "water", "food", "co2"],
    "value_per_person": [0.90, 5.00, 3000, 1.10],
    "unit": ["kg", "kg", "kcal", "kg"],
    "period": ["day", "day", "day", "day"],
    "data_status": ["mock", "mock", "mock", "mock"]
}

# Create a Pandas DataFrame
df = pd.DataFrame(data)

# Save it as a CSV file
output_path = project_root / "data" / "mock" / "resource_requirements.csv"
df.to_csv(output_path, index=False)

print("Mock dataset created successfully!")
print(df)
print(f"\nSaved at: {output_path}")
