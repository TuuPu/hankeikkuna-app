import requests

class TeematFetcher:
    BASE_URL = "https://api.hankeikkuna.fi/api/v2/teemat"

    def get_teemat(self):
        response = requests.get(self.BASE_URL)
        if response.status_code != 200:
            raise Exception(f"GET failed: {response.status_code}")
        return response.json().get("result", [])