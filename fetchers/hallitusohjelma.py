import requests
import pandas as pd

class HallitusohjelmaFetcher:
    BASE = "https://api.hankeikkuna.fi/api/v2/hallitusohjelmat"

    def search_rakenne_elementit(self, payload: dict) -> pd.DataFrame:
        url = self.BASE + "/rakenneElementit/haku"
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"POST failed: {response.status_code}")

        result = response.json().get("result", [])
        return pd.DataFrame(result)

    def get_valitavoite_tyypit(self):
        return self._get("/valitavoiteTyypit")

    def get_toimenpiteet(self):
        return self._get("/toimenpiteet")

    def get_rakenne_elementti_tyypit(self):
        return self._get("/rakenneElementtiTyypit")

    def get_painopistealueet(self):
        return self._get("/painopistealueet")

    def get_karkihankkeet(self):
        return self._get("/karkihankkeet")

    def get_hallitukset(self):
        return self._get("/hallitukset")

    def _get(self, path: str):
        url = self.BASE + path
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"GET {path} failed: {response.status_code}")
        return response.json().get("result", [])
