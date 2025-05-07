import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("City-wise Coupon Redemption Map")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert percentages from strings to float values (e.g., "21.22%" → 21.22)
    df["Share of redemptions"] = df["Share of redemptions"].str.replace('%', '').astype(float)
    df["Redeemers out of total city base"] = df["Redeemers out of total city base"].str.replace('%', '').astype(float)

    # Preview data
    st.subheader("Data Preview")
    st.dataframe(df)

    # Create a pydeck layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[Longitude, Latitude]',
        get_radius="Redeemers",  # Circle size based on Redeemers count
        radius_scale=15,
        get_fill_color="""
            [255 * (1 - Redeemers / 3300), 
             100 + 100 * (Share of redemptions > 20), 
             150]
        """,
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=df["Latitude"].mean(),
        longitude=df["Longitude"].mean(),
        zoom=4.2,
        pitch=0,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "text": "{City}\nRedeemers: {Redeemers}\nShare: {Share of redemptions}%\nBase Share: {Redeemers out of total city base}%"
        }
    ))
else:
    st.info("Upload a CSV with columns: City, Latitude, Longitude, Redeemers, Share of redemptions, Redeemers out of total city base")
