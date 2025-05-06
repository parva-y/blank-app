import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("City-wise Coupon Redemption Map")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Show raw data
    st.subheader("Raw Data")
    st.dataframe(df)

    # Create Pydeck layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[Longitude, Latitude]',
        get_radius=50000,
        get_fill_color="""
            [255 * (1 - Redeemers / max(Redeemers)), 
             100, 
             150]
        """,
        pickable=True,
        auto_highlight=True,
    )

    # Set map view
    view_state = pdk.ViewState(
        latitude=df["Latitude"].mean(),
        longitude=df["Longitude"].mean(),
        zoom=4.5,
        pitch=0,
    )

    # Display map
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{City}\nRedeemers: {Redeemers}\nShare: {Share of redemptions}\nBase Share: {Redeemers out of total city base}"}
    ))
else:
    st.info("Please upload a CSV with columns: City, Latitude, Longitude, Redeemers, Share of redemptions, Redeemers out of total city base")
