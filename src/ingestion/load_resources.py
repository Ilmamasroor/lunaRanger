
import pandas as pd
from pathlib import Path


def load_resource_data():
    # Find the project root directory
    project_root = Path(__file__).resolve().parents[2]

    # Locate the CSV file
    file_path = project_root / "data" / "mock" / "resource_requirements.csv"

    # Load CSV into a DataFrame
    df = pd.read_csv(file_path)

    return df


if __name__ == "__main__":
    resources_df = load_resource_data()

    print("Resource data loaded successfully!")
    print(resources_df)
    print("\nDataset information:")
    print(resources_df.info())
