import requests

class TyypitFetcher:
    BASE_URL = "https://api.hankeikkuna.fi/api/v2/tyypit"

    def get_kohteen_valmisteluvaiheet(self):
        response = requests.get(f"{self.BASE_URL}/kohteenValmisteluvaiheet")
        if response.status_code != 200:
            raise Exception(f"GET failed: {response.status_code}")
        return response.json().get("result", [])

    def get_he_saados_tyypit(self):
        response = requests.get(f"{self.BASE_URL}/heSaadosTyypit")
        if response.status_code != 200:
            raise Exception(f"GET failed: {response.status_code}")
        return response.json().get("result", [])
