import streamlit as st
import folium
import requests
from streamlit_folium import st_folium

st.title("🏃‍♂️ Routenplaner: Laufroute erstellen")
st.markdown("Gib deinen gewünschten Startpunkt und eine Zielstrecke an – wir berechnen dir eine Rundroute!")

latitude = st.number_input("Breitengrad (z. B. 51.9607 für Münster)", value=51.9607, format="%.6f")
longitude = st.number_input("Längengrad (z. B. 7.6261 für Münster)", value=7.6261, format="%.6f")
route_length_km = st.slider("Gewünschte Distanz (in km)", min_value=1, max_value=20, value=5)
api_key = st.text_input("🔑 Dein OpenRouteService API-Key", type="password")

if api_key and st.button("🔄 Route berechnen"):
    try:
        url = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"
        headers = {"Authorization": api_key, "Content-Type": "application/json"}
        params = {
            "coordinates": [[longitude, latitude], [longitude, latitude]],
            "options": {"round_trip": {"length": route_length_km * 1000, "seed": 3}},
            "instructions": False
        }
        response = requests.post(url, json=params, headers=headers)

        if response.status_code != 200:
            st.error(f"Fehler bei der API-Anfrage: {response.text}")
        else:
            data = response.json()
            geometry = data['features'][0]['geometry']['coordinates']
            route_coords = [(lat, lon) for lon, lat in geometry]
            map_route = folium.Map(location=[latitude, longitude], zoom_start=14)
            folium.PolyLine(route_coords, color="blue", weight=5).add_to(map_route)
            folium.Marker([latitude, longitude], tooltip="Startpunkt").add_to(map_route)
            st_folium(map_route, width=700, height=500)

    except Exception as e:
        st.error(f"Fehler bei der Berechnung: {e}")
