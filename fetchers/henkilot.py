import requests
import pandas as pd

class HenkilotFetcher:
    BASE_URL = "https://api.hankeikkuna.fi/api/v2/henkilot/haku"

    def search(self, payload: dict) -> pd.DataFrame:
        """
        POST search to henkilot endpoint with filters.
        """
        response = requests.post(self.BASE_URL, json=payload)
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")

        result = response.json().get("result", [])
        if not result:
            return pd.DataFrame()

        # Flatten key fields
        data = []
        for item in result:
            data.append({
                "uuid": item.get("uuid"),
                "etunimi": item.get("etunimi"),
                "sukunimi": item.get("sukunimi"),
                "nimike": item.get("nimike"),
                "tyonantaja": item.get("tyonantaja", {}).get("nimi", {}).get("fi"),
                "organisaatio": item.get("organisaatio", {}).get("nimi", {}).get("fi")
            })

        return pd.DataFrame(data)
