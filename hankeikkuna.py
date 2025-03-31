import streamlit as st
import io
from datetime import date
import pandas as pd
import pprint

from utils.normalize import flatten_items
from fetchers.asettajat import AsettajatFetcher
from fetchers.kohteet import KohteetFetcher
from fetchers.henkilot import HenkilotFetcher
from fetchers.hallitusohjelma import HallitusohjelmaFetcher
from fetchers.teemat import TeematFetcher
from fetchers.istuntokaudet import IstuntokaudetFetcher
from fetchers.tyypit import TyypitFetcher

st.set_page_config(page_title="Hankeikkuna API Tool", layout="wide")
st.title("💡 Hankeikkuna API Explorer")

tabs = st.tabs([
    "Asettajat",
    "Kohteet",
    "Henkilöt",
    "Teemat"
])

# Asettajat
with tabs[0]:
    fetcher = AsettajatFetcher()
    st.subheader("Asettajat")

    # Filter controls
    col1, col2, col3 = st.columns(3)
    with col1:
        search_type = st.selectbox("Search by", ["Name", "Abbreviation"])
    with col2:
        lang = st.selectbox("Language", ["fi", "sv", "en"])
    with col3:
        status_filter = st.selectbox("Status", ["All", "Active", "Inactive"])

    search_input = st.text_input("Enter search text")

    if st.button("Fetch Asettajat"):
        try:
            df = fetcher.fetch_all()

            if df.empty:
                st.warning("No data found.")
            else:
                # Filter by status
                if status_filter != "All":
                    active_bool = True if status_filter == "Active" else False
                    df = df[df["aktiivinen"] == active_bool]

                # Filter by search term
                if search_input:
                    column = "nimi_" + lang if search_type == "Name" else "lyhenne_" + lang
                    if column in df.columns:
                        df = df[df[column].str.contains(search_input, case=False, na=False)]

                st.success(f"Found {len(df)} asettajat.")
                st.dataframe(df)

                if not df.empty:
                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False)
                    st.download_button(
                        label="Download as CSV",
                        data=csv_buffer.getvalue(),
                        file_name="asettajat.csv",
                        mime="text/csv"
                    )

        except Exception as e:
            st.error(f"Error fetching data: {e}")

# Kohteet
with tabs[1]:
    fetcher = KohteetFetcher()
    st.subheader("Kohteet (Projects)")

    with st.expander("🔍 Search Filters"):
        col1, col2 = st.columns(2)

        with col1:
            search_text = st.text_input("Teksti (free-text search)")
            selected_types = st.multiselect("Tyyppi", ["HANKE", "LAINSAADANTO"])
            selected_statuses = st.multiselect("Tila", ["SUUNNITTEILLA", "KAYNNISSA", "PAATTYNYT"])
            #asettaja_uuid = st.text_input("Asettaja UUID")
            #teema_uuid = st.text_input("Teema UUID")
            valmisteluvaihe = st.text_input("Valmisteluvaihe")
            #toimenpide_uuid = st.text_input("Toimenpide UUID")
            #hallitus_elementti_uuid = st.text_input("Hallitusohjelma Elementti UUID")
            #hallitus_valitavoite_uuid = st.text_input("Hallitusohjelma Välitavoite UUID")
            lainsaadanto_tehtavaluokka = st.text_input("Lainsäädäntötehtäväluokka")
            toimielin_tyyppi = st.text_input("Toimielin Tyyppi")

        with col2:
            tunnus = st.text_input("Tunnus")
            #asiasanat = st.text_input("Asiasanat (comma-separated)")
            #ylatason_kohde_uuid = st.text_input("Ylätason Kohde UUID")
            #strategia_tyyppi = st.text_input("Strategia Tyyppi")
            #he_istuntokausi_uuid = st.text_input("HE Istuntokausi UUID")
            #etappi_tyyppi = st.text_input("Etappi Tyyppi")
            asettamis_alku = st.date_input("Asettamispäivä Alku", value=None)
            asettamis_loppu = st.date_input("Asettamispäivä Loppu", value=None)
            muokattu_alku = st.date_input("Muokattu Päivä Alku", value=None)
            muokattu_loppu = st.date_input("Muokattu Päivä Loppu", value=None)
            etappi_alku = st.date_input("Etappi Alku", value=None)
            etappi_loppu = st.date_input("Etappi Loppu", value=None)

        size = st.slider("Number of results", 10, 1000, 50, key="kohteet_slider")

    if st.button("Search Kohteet"):
        try:
            payload = fetcher.default_payload()
            payload.pop("sort", None)
            payload["size"] = size
            payload["teksti"] = search_text
            payload["tyyppi"] = selected_types
            payload["tila"] = selected_statuses

            if tunnus:
                payload["tunnus"] = [tunnus]
            #if asettaja_uuid:
            #    payload["asettajaUuid"] = [asettaja_uuid]
            #if teema_uuid:
            #    payload["teemaUuid"] = [teema_uuid]
            if valmisteluvaihe:
                payload["valmisteluvaihe"] = [valmisteluvaihe]
            #if toimenpide_uuid:
            #    payload["toimenpideUuid"] = [toimenpide_uuid]
            #if hallitus_elementti_uuid:
            #    payload["hallitusohjelmaElementtiUuid"] = [hallitus_elementti_uuid]
            #if hallitus_valitavoite_uuid:
            #    payload["hallitusohjelmaValitavoiteUuid"] = [hallitus_valitavoite_uuid]
            if lainsaadanto_tehtavaluokka:
                payload["lainsaadantoTehtavaluokka"] = [lainsaadanto_tehtavaluokka]
            if toimielin_tyyppi:
                payload["toimielinTyyppi"] = [toimielin_tyyppi]
            #if strategia_tyyppi:
            #    payload["strategiaTyyppi"] = [strategia_tyyppi]
            #if he_istuntokausi_uuid:
            #    payload["heIstuntokausiUuid"] = [he_istuntokausi_uuid]
            #if ylatason_kohde_uuid:
            #    payload["ylatasonKohdeUuid"] = [ylatason_kohde_uuid]
            #if etappi_tyyppi:
            #    payload["etappiTyyppi"] = [etappi_tyyppi]
            #if asiasanat:
            #    payload["asiasanat"] = [s.strip() for s in asiasanat.split(",")]

            if asettamis_alku:
                payload["asettamisPaivaAlku"] = asettamis_alku.strftime("%Y-%m-%d")
            if asettamis_loppu:
                payload["asettamisPaivaLoppu"] = asettamis_loppu.strftime("%Y-%m-%d")
            if muokattu_alku:
                payload["muokattuPaivaAlku"] = muokattu_alku.strftime("%Y-%m-%d")
            if muokattu_loppu:
                payload["muokattuPaivaLoppu"] = muokattu_loppu.strftime("%Y-%m-%d")
            if etappi_alku:
                payload["etappiAlkamisPaivaAlku"] = etappi_alku.strftime("%Y-%m-%d")
            if etappi_loppu:
                payload["etappiAlkamisPaivaLoppu"] = etappi_loppu.strftime("%Y-%m-%d")

            cleaned_payload = fetcher.clean_payload(payload)
            st.subheader("🔎 Cleaned request payload")

            df = fetcher.search(cleaned_payload)

            if df.empty:
                st.warning("No results found.")
            else:
                st.success(f"Found {len(df)} kohteet.")
                st.dataframe(df.reset_index(drop=True))

                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv_buffer.getvalue(),
                    file_name="kohteet.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Error fetching kohteet: {e}")
# Henkilöt
with tabs[2]:
    fetcher = HenkilotFetcher()
    st.subheader("Henkilöt (People Search)")

    # --- Filters ---
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First name (etunimi)")
        occupation = st.text_input("Occupation (nimike)")
    with col2:
        last_name = st.text_input("Last name (sukunimi)")
        employer = st.text_input("Employer (työnantaja)")

    size = st.slider("Number of results", 10, 100, 50, key="henkilot_slider")

    if st.button("Search Henkilöt"):
        try:
            # Build payload
            payload = {
                "size": size
            }

            # Add filters only if they have values
            if first_name:
                payload["etunimi"] = [first_name]
            if last_name:
                payload["sukunimi"] = [last_name]
            if occupation:
                payload["nimike"] = [occupation]
            if employer:
                payload["tyonantaja"] = [employer]

            df = fetcher.search(payload)

            if df.empty:
                st.warning("No results found.")
            else:
                st.success(f"Found {len(df)} results.")
                st.dataframe(df)

                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv_buffer.getvalue(),
                    file_name="henkilot.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Error fetching henkilöt: {e}")


# Teemat
with tabs[3]:
    fetcher = TeematFetcher()
    st.subheader("Teemat (Themes)")

    try:
        raw = fetcher.get_teemat()
        df = flatten_items(raw, name_field="nimi", extra_fields=["uuid"])

        if df.empty:
            st.warning("No themes found.")
        else:
            st.success(f"Found {len(df)} themes.")
            st.dataframe(df)

            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="Download as CSV",
                data=csv_buffer.getvalue(),
                file_name="teemat.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error fetching themes: {e}")