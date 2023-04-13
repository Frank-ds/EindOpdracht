import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plost
import pickle
import numpy as np
from datetime import datetime
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt

# load data
conv_path = r"c:\users\frank\Documents\DME\Eindopdracht_without_raw\data\Processed"
with open(conv_path + "\E214_230128.pkl", "rb") as f:
    df_0128 = pickle.load(f)

with open(conv_path + "\E214_230129.pkl", "rb") as f:
    df_0129 = pickle.load(f)

with open(conv_path + "\E214_230130.pkl", "rb") as f:
    df_0130 = pickle.load(f)

with open(conv_path + "\E214_230131.pkl", "rb") as f:
    df_0131 = pickle.load(f)

with open(conv_path + "\E214_A.pkl", "rb") as f:
    df = pickle.load(f)

#
Total_Eng_nrg = np.max(df["engine_used_energy"])
Drive_nrg = np.max(df["drive_energy"])
Hydr_nrg = np.max(df["hydr_energy"])
Idle_nrg = np.max(df["idle_energy"])
Work_nrg = np.max(df["working_energy"])

drive_energy_perc = round(Drive_nrg * 100 / Total_Eng_nrg, 2)
hydr_energy_perc = round(Hydr_nrg * 100 / Total_Eng_nrg, 2)
work_energy_perc = round(Work_nrg * 100 / Total_Eng_nrg, 2)
idle_energy_perc = round(Idle_nrg * 100 / Total_Eng_nrg, 2)

mean_drive_power = np.mean(df["drive_power"])
mean_hydr_power = np.mean(df["hydr_power"])
mean_work_power = np.mean(df["working_power"])
mean_idle_power = np.mean(df["idle_power"])
mean_engine_power = np.mean(df.EnginePower)


Nrg_list = [Total_Eng_nrg, Drive_nrg, Hydr_nrg, Idle_nrg, Work_nrg]
Nrg_N_list = ["Total_Eng_nrg", "Drive_nrg", "Hydr_nrg", "Idle_nrg", "Work_nrg"]


################################ Dashboard
st.set_page_config(layout="wide", initial_sidebar_state="expanded")


# def streamlit_menu(example=1):
#     if example == 1:
#         # 1. as sidebar menu
#         with st.sidebar:
#             selected = option_menu(
#                 menu_title="Main Menu",  # required
#                 options=["Home", "Projects", "Contact"],  # required
#                 icons=["house", "book", "envelope"],  # optional
#                 menu_icon="cast",  # optional
#                 default_index=0,  # optional
#             )
#         return selected


# selected = streamlit_menu(example=1)

if selected == "Home":
    st.title(f"You have selected {selected}")
if selected == "Projects":
    st.title(f"You have selected {selected}")
if selected == "Contact":
    st.title(f"You have selected {selected}")

st.sidebar.header("Dashboard `init`")

st.sidebar.subheader("Heat map parameter")
time_hist_color = st.sidebar.selectbox("Color by", ("temp_min", "temp_max"))

st.sidebar.subheader("Donut chart parameter")
donut_theta = st.sidebar.selectbox("Select data", ("q2", "q3"))

st.sidebar.subheader("Line chart parameters")
plot_data = st.sidebar.multiselect(
    "Select data", ["temp_min", "temp_max"], ["temp_min", "temp_max"]
)
start_time = st.slider(
    "When do you start?", value=datetime(2020, 1, 1, 9, 30), format="MM/DD/YY - hh:mm"
)
st.write("Start time:", start_time)

st.sidebar.markdown(
    """
---
Created with ❤️.
"""
)


# Row A
st.markdown("### Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Drive energy ", f"{round(Drive_nrg, 2)} KWh", f"{drive_energy_perc} %")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# Row B
c1, c2 = st.columns((5, 5))
with c1:
    st.subheader("Box plot")
    fig = px.box(df, x="Truck_State", y="Engine_used_energy", color="Truck_State")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with c2:
    st.subheader("Energy split")
    fig1 = px.bar(x=Nrg_list, y=Nrg_N_list)
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)


# Row C
st.markdown("### test plot")
# st.line_chart(df, x="timestamps", y="Engine_used_energy")
fig1 = px.scatter(df, x="Truck_State", y="Engine_used_energy", color="Truck_State")
st.plotly_chart(fig1, theme="streamlit", use_container_width=True)


chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x="EnginePower",
        y="Engine_used_energy",
        color="Truck_State",
    )
    .interactive()
)
st.altair_chart(chart, theme="streamlit", use_container_width=True)
