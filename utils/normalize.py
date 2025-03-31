import pandas as pd

def flatten_items(data, name_field="nimi", extra_fields=None):
    if not data or not isinstance(data, list):
        return pd.DataFrame()

    rows = []
    for item in data:
        if not isinstance(item, dict):
            continue

        row = {}

        # Flatten language field like 'nimi' or 'kuvaus'
        name_data = item.get(name_field)
        if isinstance(name_data, dict):
            row["name_fi"] = name_data.get("fi")
            row["name_sv"] = name_data.get("sv")
            row["name_en"] = name_data.get("en")
        else:
            row["name_fi"] = name_data

        # Remove the original nested field to avoid rendering issues
        item.pop(name_field, None)

        # Copy extra fields
        if extra_fields:
            for field in extra_fields:
                value = item.get(field)
                if isinstance(value, dict):
                    row[field + "_fi"] = value.get("fi")
                    row[field + "_sv"] = value.get("sv")
                    row[field + "_en"] = value.get("en")
                elif isinstance(value, (str, int, float, bool)) or value is None:
                    row[field] = value
                else:
                    row[field] = str(value)

        rows.append(row)

    return pd.DataFrame(rows)
