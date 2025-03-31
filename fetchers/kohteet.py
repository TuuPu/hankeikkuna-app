import requests
import pandas as pd

class KohteetFetcher:
    BASE_URL = "https://api.hankeikkuna.fi/api/v2/kohteet/haku"

    def search(self, payload: dict) -> pd.DataFrame:
        """
        POST search to kohteet endpoint with full filter support.
        """
        cleaned_payload = self.clean_payload(payload)

        response = requests.post(self.BASE_URL, json=cleaned_payload)
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")

        result = response.json().get("result", [])
        if not result:
            return pd.DataFrame()

        data = []
        for item in result:
            kohde = item.get("kohde", {})
            data.append({
                "uuid": kohde.get("uuid"),
                "nimi_fi": kohde.get("nimi", {}).get("fi"),
                "kuvaus_fi": kohde.get("kuvaus", {}).get("fi"),
                "tila": kohde.get("tila"),
                "tunnus": kohde.get("tunnus"),
                "asettajaUuid": kohde.get("asettajaUuid"),
                "asettamisPaiva": kohde.get("asettamisPaiva"),
                "aloitusPaiva": kohde.get("aloitusPaiva"),
                "valmistumisPaiva": kohde.get("valmistumisPaiva"),
                "valmisteluvaihe": kohde.get("valmisteluvaihe"),
                "lainsaadanto": kohde.get("liittyyLainsaadantoon"),
                "talousarvio": kohde.get("liittyyTalousarvioon"),
                "asiasanat": ", ".join(
    str(tag.get("fi")) for tag in item.get("asiasanat", [])
    if isinstance(tag, dict) and tag.get("fi") is not None
) if isinstance(item.get("asiasanat"), list) else None,
            })

        df = pd.DataFrame(data)

        # Drop rows where all visible fields are None or empty
        columns_to_check = [
            "nimi_fi", "kuvaus_fi", "tila", "tunnus", "asettajaUuid",
            "asiasanat", "asettamisPaiva", "aloitusPaiva", "valmistumisPaiva"
        ]

        df = df.dropna(subset=columns_to_check, how="all").reset_index(drop=True)
        return df

    def clean_payload(self, payload: dict) -> dict:
        """
        Removes fields that are None, empty strings, or empty lists.
        """
        return {
            k: v for k, v in payload.items()
            if v not in [None, "", []]
        }

    def default_payload(self) -> dict:
        """
        Returns a full default payload for kohteet search.
        """
        return {
            "searchAfter": [],
            "size": 50,
            "sort": [{"field": "asettamisPaiva", "order": "ASC"}],
            "uuid": [],
            "tunnus": [],
            "tyyppi": [],
            "asettajaUuid": [],
            "asiasanat": [],
            "teemaUuid": [],
            "asettamisPaivaAlku": None,
            "asettamisPaivaLoppu": None,
            "tila": [],
            "teksti": "",
            "toimenpideUuid": [],
            "hallitusohjelmaElementtiUuid": [],
            "hallitusohjelmaValitavoiteUuid": [],
            "muokattuPaivaAlku": None,
            "muokattuPaivaLoppu": None,
            "etappiAlkamisPaivaAlku": None,
            "etappiAlkamisPaivaLoppu": None,
            "etappiTyyppi": [],
            "ylatasonKohdeUuid": [],
            "lainsaadantoTehtavaluokka": [],
            "toimielinTyyppi": [],
            "strategiaTyyppi": [],
            "valmisteluvaihe": [],
            "heIstuntokausiUuid": []
        }
