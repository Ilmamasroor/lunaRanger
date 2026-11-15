
from src.ingestion.load_resources import load_resource_data
from src.processing.clean_resources import clean_resource_data
from src.validation.validate_resources import validate_resource_data


PARAMETER_METADATA = {
    "oxygen": {
        "parameter_id": "crew_oxygen_consumption",
        "flow_type": "consumption",
        "source": None,
        "assumptions": [],
        "notes": "Mock daily crew oxygen demand"
    },
    "water": {
        "parameter_id": "crew_water_requirement",
        "flow_type": "consumption",
        "source": None,
        "assumptions": [],
        "notes": "Water usage categories need clarification"
    },
    "food": {
        "parameter_id": "crew_food_energy",
        "flow_type": "consumption",
        "source": None,
        "assumptions": [],
        "notes": "Daily food energy requirement"
    },
    "co2": {
        "parameter_id": "crew_co2_production",
        "flow_type": "production",
        "source": None,
        "assumptions": [],
        "notes": "Mock daily crew CO2 production"
    }
}


def map_resource_data(df, crew_size=4):

    parameters = []

    for _, row in df.iterrows():

        resource = row["resource"]
        metadata = PARAMETER_METADATA[resource]

        parameter = {
            "parameter_id": metadata["parameter_id"],
            "resource": resource,
            "flow_type": metadata["flow_type"],
            "value_per_person": float(row["value_per_person"]),
            "unit": row["unit"],
            "period": {
                "value": 1,
                "unit": row["period"]
            },
            "data_status": row["data_status"],
            "source": metadata["source"],
            "assumptions": metadata["assumptions"],
            "notes": metadata["notes"]
        }

        parameters.append(parameter)

    config = {
        "schema_version": "1.1",
        "mission": {
            "crew_size": crew_size
        },
        "parameters": parameters
    }

    return config


if __name__ == "__main__":

    raw_df = load_resource_data()
    cleaned_df = clean_resource_data(raw_df)

    errors = validate_resource_data(cleaned_df)

    if errors:
        print("Cannot map invalid data:")
        for error in errors:
            print("-", error)

    else:
        config = map_resource_data(cleaned_df)

        print("Data mapping successful!")
        print(config)
