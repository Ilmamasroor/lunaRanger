
import pandas as pd

from src.processing.clean_resources import clean_resource_data
from src.ingestion.load_resources import load_resource_data

def validate_resource_data(df):

    errors = []

    required_columns = [
        "resource",
        "value_per_person",
        "unit",
        "period",
        "data_status"
    ]

    # Check required columns
    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        return [f"Missing columns: {missing_columns}"]

    # Check missing values
    if df[required_columns].isnull().any().any():
        errors.append("Dataset contains missing values.")

    # Check duplicate resources
    if df["resource"].duplicated().any():
        errors.append("Duplicate resource records found.")

    # Check numeric values
    values = pd.to_numeric(
        df["value_per_person"],
        errors="coerce"
    )

    if values.isnull().any():
        errors.append("Resource values must be numeric.")

    elif (values < 0).any():
        errors.append("Resource values cannot be negative.")

    # Check expected units for our mock resources
    expected_units = {
        "oxygen": "kg",
        "water": "kg",
        "food": "kcal",
        "co2": "kg"
    }

    for _, row in df.iterrows():
        resource = row["resource"]

        if resource not in expected_units:
            errors.append(f"Unknown resource: {resource}")

        elif row["unit"] != expected_units[resource]:
            errors.append(f"Invalid unit for {resource}.")

    # Check period
    if not (df["period"] == "day").all():
        errors.append("All resource periods must be day.")

    return errors

if __name__ == "__main__":

    raw_df = load_resource_data()
    cleaned_df = clean_resource_data(raw_df)

    validation_errors = validate_resource_data(cleaned_df)

    if validation_errors:
        print("Validation failed!")

        for error in validation_errors:
            print("-", error)

    else:
        print("Validation successful!")
        print("All resource records passed the checks.")

    print("\nTesting invalid data...")
