import requests
import pandas as pd

class AsettajatFetcher:
    BASE_URL = "https://api.hankeikkuna.fi/api/v2/asettajat"

    def fetch_all(self):
        """Fetch all asettajat and return as a pandas DataFrame."""
        response = requests.get(self.BASE_URL)
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")

        result = response.json().get("result", [])
        if not result:
            return pd.DataFrame()

        # Normalize nested fields into a clean DataFrame
        data = []
        for item in result:
            data.append({
                "uuid": item.get("uuid"),
                "nimi_fi": item.get("nimi", {}).get("fi"),
                "nimi_sv": item.get("nimi", {}).get("sv"),
                "nimi_en": item.get("nimi", {}).get("en"),
                "lyhenne_fi": item.get("lyhenne", {}).get("fi"),
                "lyhenne_sv": item.get("lyhenne", {}).get("sv"),
                "lyhenne_en": item.get("lyhenne", {}).get("en"),
                "aktiivinen": item.get("aktiivinen")
            })

        return pd.DataFrame(data)