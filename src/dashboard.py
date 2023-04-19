from settings import settings
import pathlib as Path
import pandas as pd
import dash_settings
from datetime import datetime, timedelta
from datetime import datetime, timezone
from streamlit_option_menu import option_menu
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# NRG_LIST = dash_settings.Nrg_list
# NRG_N_LIST = dash_settings.Nrg_N_list
SLIDER_LIST = dash_settings.SLIDER_LIST
GPS_LIST = dash_settings.GPS_LIST

df = dash_settings.df
df_0128 = dash_settings.df_0128
df_0129 = dash_settings.df_0129
df_0130 = dash_settings.df_0130
df_0131 = dash_settings.df_0131


######################################## Dashboard ########################################
st.set_page_config(layout="wide", initial_sidebar_state="expanded")


def streamlit_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "GPS"],
            icons=["sliders", "bar-chart-line", "geo"],
            menu_icon="clipboard-data",
            default_index=0,
        )
    return selected


######################################## Home tab ########################################
selected = streamlit_menu()

if selected == "Home":
    st.title(f" {selected}")
    # slider config
    min_time = datetime(2023, 1, 28, 0, 0)
    max_time = datetime(2023, 2, 14, 23, 59)
    init_min_time = datetime(2023, 2, 6, 0, 0)
    init_max_time = datetime(2023, 2, 6, 7, 0)
    step = timedelta(minutes=30)

    # Create double-ended slider for time range
    start_time, end_time = st.slider(
        "Select time range",
        min_value=min_time,
        max_value=max_time,
        value=(init_min_time, init_max_time),
        step=step,
        format="MM/DD/YY - hh:mm",
    )

    # Convert start_time to UTC timezone
    start_time_utc = start_time.replace(tzinfo=timezone.utc)
    end_time_utc = end_time.replace(tzinfo=timezone.utc)

    df_filt = df.copy()
    df_filt = df.loc[:, SLIDER_LIST]
    # Filter dataframe based on time range
    df_filtered = df_filt[
        (df_filt.index >= start_time_utc) & (df_filt.index <= end_time_utc)
    ]

    Eng_nrg_dash = dash_settings.accumulate_energy(df_filtered, "engine_power")
    drive_nrg_dash = dash_settings.accumulate_energy(df_filtered, "drive_power")
    hydr_nrg_dash = dash_settings.accumulate_energy(df_filtered, "hydr_power")
    idle_nrg_dash = dash_settings.accumulate_energy(df_filtered, "idle_power")
    work_nrg_dash = dash_settings.accumulate_energy(df_filtered, "working_power")

    Nrg_list = [
        Eng_nrg_dash,
        drive_nrg_dash,
        hydr_nrg_dash,
        idle_nrg_dash,
        work_nrg_dash,
    ]
    Nrg_N_list = ["Total_Eng_nrg", "Drive_nrg", "Hydr_nrg", "Idle_nrg", "Work_nrg"]

    print(Eng_nrg_dash)

    # Row A
    st.markdown("### Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("drive energy ", f"{drive_nrg_dash} KWh")
    col2.metric("Hydraulic energy", f"{hydr_nrg_dash} KWh")
    col3.metric("Working energy", f"{work_nrg_dash} KWh")
    col4.metric("Idle energy", f"{idle_nrg_dash} KWh")
    col5.metric("engine energy", f"{Eng_nrg_dash} KWh")

    # Row B
    c1, c2 = st.columns((5, 5))
    with c1:
        st.subheader("Box plot")
        fig = px.box(
            df_filtered, x="truck_state", y="engine_power", color="truck_state"
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # Barchart
    with c2:
        st.subheader("Energy split")
        fig1 = px.bar(
            x=Nrg_list,
            y=Nrg_N_list,
            text_auto=True,
        )

        fig1.update_traces(
            textposition="auto",
            hovertemplate="%{y:.2f}",
        )
        fig1.update_layout(xaxis=dict(tickmode="array", tickvals=[]))
        fig.update_layout(xaxis=dict(showticklabels=False))
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

########################################Day tab########################################
# if selected == "per day":
#     st.title(f" {selected}")

#     # Example usage
#     dfs = {"df1": df_0128, "df2": df_0129, "df3": df_0130, "df3": df_0131}
#     results = {}
#     for name, df in dfs.items():
#         results[name] = dash_settings.power_accumulation(df)
#     df_results = pd.DataFrame.from_dict(results, orient="index")

#     dataframes = {
#         "28-Jan-2023": df_0128,
#         "29-Jan-2023": df_0129,
#         "30-Jan-2023": df_0130,
#         "31-Jan-2023": df_0131,
#     }

#     # Create a multiselect widget with the keys of the dictionary as options
#     selected_dataframes = st.multiselect(
#         "Select day(s)", options=list(dataframes.keys())
#     )

#     # Retrieve the selected dataframes from the dictionary and do some analysis
#     if selected_dataframes:
#         for df_key in selected_dataframes:
#             df = dataframes[df_key]

#     if selected_dataframes:
#         concat_df = pd.concat(
#             [dataframes[df_key] for df_key in selected_dataframes], axis=0
#         )

#     df_daily = concat_df.groupby(pd.Grouper(freq="D")).max()

#     # Bar chart
#     st.subheader("Energy per function")
#     fig1 = px.bar(
#         df_daily,
#         x=df_daily.index,
#         y=["drive_energy", "hydr_energy", "idle_energy", "working_energy"],
#         # barmode="group",
#         # text_auto=True,
#     )

#     fig1.update_traces(
#         # text=df_daily.values.flatten(),
#         textposition="auto",
#         hovertemplate="%{y:.2f}",
#     )
#     fig1.update_xaxes(title_text="Day")
#     fig1.update_xaxes(title_font=dict(size=16, family="Arial"))
#     fig1.update_yaxes(title_text="Energy per day in [KW/h]")
#     fig1.update_yaxes(title_font=dict(size=16, family="Arial"))
#     st.plotly_chart(fig1, theme="streamlit", use_container_width=True)


######################################## GPS tab########################################
if selected == "GPS":
    st.title(f" {selected}")

    # slider config
    min_time = datetime(2023, 1, 28, 0, 0)
    max_time = datetime(2023, 2, 14, 23, 59)
    init_min_time = datetime(2023, 2, 6, 0, 0)
    init_max_time = datetime(2023, 2, 6, 7, 0)
    step = timedelta(minutes=30)

    # Create double-ended slider for time range
    start_time, end_time = st.slider(
        "Select time range",
        min_value=min_time,
        max_value=max_time,
        value=(init_min_time, init_max_time),
        step=step,
        format="MM/DD/YY - hh:mm",
    )

    # Convert start_time to UTC timezone
    start_time_utc = start_time.replace(tzinfo=timezone.utc)
    end_time_utc = end_time.replace(tzinfo=timezone.utc)

    df_filt = df.copy()
    df_filt = df.loc[:, GPS_LIST]
    # Filter dataframe based on time range
    df_filtered = df_filt[
        (df_filt.index >= start_time_utc) & (df_filt.index <= end_time_utc)
    ]

    # GPS plot
    st.subheader("GPS plot")
    fig2 = px.scatter_mapbox(
        df_filtered,
        lat="lat",
        lon="lon",
        hover_data=["vehicle_speed", "lift_height"],
        color="truck_state",
        color_continuous_scale=[
            (0, "Green"),
            (0.5, " yellow"),
            (0.7, "red"),
            (1, "Purple"),
        ],
        zoom=15,
        height=900,
    )
    fig2.update_layout(
        mapbox_style="open-street-map",
        mapbox_layers=[
            {
                "below": "traces",
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ],
            }
        ],
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
