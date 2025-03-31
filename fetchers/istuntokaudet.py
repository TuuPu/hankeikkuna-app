import requests

class IstuntokaudetFetcher:
    BASE_URL = "https://api.hankeikkuna.fi/api/v2/istuntokaudet"

    def get_istuntokaudet(self):
        response = requests.get(self.BASE_URL)
        if response.status_code != 200:
            raise Exception(f"GET failed: {response.status_code}")
        return response.json().get("result", [])