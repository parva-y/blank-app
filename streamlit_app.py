import streamlit as st
import pandas as pd
import pydeck as pdk

# Load city data
data = pd.DataFrame({
    'City': [...],
    'Lat': [...],
    'Lon': [...],
    'Txn_Franchisee': [...],
    'Frequency': [...],
})

# Pydeck map
layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position='[Lon, Lat]',
    get_radius=50000,
    get_fill_color="[255 * (1 - Frequency/3300), 100, 200]",
    pickable=True
)

view_state = pdk.ViewState(latitude=21, longitude=78, zoom=4)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{City}\n{Frequency} Txns"}))
