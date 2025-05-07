import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("City-wise Coupon Redemption Map")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert percentages to float
    df["Share of redemptions"] = df["Share of redemptions"].str.replace('%', '').astype(float)
    df["Redeemers out of total city base"] = df["Redeemers out of total city base"].str.replace('%', '').astype(float)

    # Normalize Redeemers for color scaling
    max_redeemers = df["Redeemers"].max()
    df["fill_color"] = df["Redeemers"].apply(
        lambda x: [255 * (1 - x / max_redeemers), 100, 150]
    )

    # Preview data
    st.subheader("Data Preview")
    st.dataframe(df)

    # Create map layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[Longitude, Latitude]',
        get_radius="Redeemers",
        radius_scale=15,
        get_fill_color="fill_color",
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
