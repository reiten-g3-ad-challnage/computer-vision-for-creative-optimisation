import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
import cv2

# read csv from a github repo
rows = 10
df = pd.read_csv("../data/merged_data.csv")
current_df = df.iloc[:rows]

st.set_page_config(
    page_title = 'Computer Vision for Creative Optimisation',
    page_icon = '✅',
    layout = 'wide'
)


st.title("Computer Vision for Creative Optimisation")


# creating a single-element container.
placeholder = st.empty()


with placeholder.container():
    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)

    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Start Frame")
        image = cv2.imread("../data/extracted_images/5b4d2cc82bf11b1fa80b366fdd7a5867"+"/start_frame.png")
        st.image(image)
    with fig_col2:
        st.markdown("### End Frame")
        image = cv2.imread("../data/extracted_images/5b4d2cc82bf11b1fa80b366fdd7a5867"+"/end_frame.png")
        st.image(image)

    fig_col4, fig_col5 = st.columns(2)
    with fig_col4:
        st.markdown("### Logo Detection")
        #fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'marital')
        image = cv2.imread("../data/detected_logo/5b4d2cc82bf11b1fa80b366fdd7a5867detected_logo.jpg")
        st.image(image)
    with fig_col5:
        st.markdown("### Edge detection")
        image = cv2.imread("../data/detected_edges/5b4d2cc82bf11b1fa80b366fdd7a5867detected_edge.jpg")
        st.image(image)
    fig_col6,_ = st.columns(2)
    with fig_col6:
        st.markdown("### Detected CTA")
        #fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'marital')
        image = cv2.imread("../data/detected_cta/5b4d2cc82bf11b1fa80b366fdd7a5867detected_cta.jpg")
        st.image(image)

    
    st.markdown("### Detailed Data View")
    def next_view():
        global rows, current_df, df
        current_df = df[rows:rows+10]
        rows = rows + 10
    st.dataframe(current_df)
    st.button("Prev")
    st.button("Next", on_click=next_view)
    
