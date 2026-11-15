
import pandas as pd

from src.ingestion.load_resources import load_resource_data


def clean_resource_data(df):
    # Keep the original DataFrame unchanged
    df = df.copy()

    # Standardize text columns
    text_columns = ["resource", "unit", "period", "data_status"]

    for column in text_columns:
        df[column] = df[column].str.strip().str.lower()

    # Ensure resource values are numeric
    df["value_per_person"] = pd.to_numeric(
        df["value_per_person"],
        errors="raise"
    )

    return df


if __name__ == "__main__":
    raw_df = load_resource_data()

    cleaned_df = clean_resource_data(raw_df)

    print("Data cleaning completed!")
    print(cleaned_df)
    print("\nData types:")
    print(cleaned_df.dtypes)
