import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
import cv2

# read csv from a github repo
df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")


st.set_page_config(
    page_title = 'Computer Vision for Creative Optimisation',
    page_icon = '✅',
    layout = 'wide'
)

# dashboard title

st.title("Computer Vision for Creative Optimisation")

# top-level filters 

job_filter = st.selectbox("Select the Job", pd.unique(df['job']))


# creating a single-element container.
placeholder = st.empty()

# dataframe filter 

df = df[df['job']==job_filter]

# near real-time / live feed simulation 

for seconds in range(200):
#while True: 
    
    df['age_new'] = df['age'] * np.random.choice(range(1,5))
    df['balance_new'] = df['balance'] * np.random.choice(range(1,5))

    # creating KPIs 
    avg_age = np.mean(df['age_new']) 

    count_married = int(df[(df["marital"]=='married')]['marital'].count() + np.random.choice(range(1,30)))
    
    balance = np.mean(df['balance_new'])

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Age ⏳", value=round(avg_age), delta= round(avg_age) - 10)
        kpi2.metric(label="Married Count 💍", value= int(count_married), delta= - 10 + count_married)
        kpi3.metric(label="A/C Balance ＄", value= f"$ {round(balance,2)} ", delta= - round(balance/count_married) * 100)

        # create two columns for charts 

        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### Start Frame")
            #fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'marital')
            image = cv2.imread("../data/extracted_images/3a3878c4fa9698438884f2288bdd1ea2"+"/start_frame.png")
            st.image(image)
        with fig_col2:
            st.markdown("### End Frame")
            image = cv2.imread("../data/extracted_images/3a3878c4fa9698438884f2288bdd1ea2"+"/end_frame.png")
            st.image(image)

        fig_col4, fig_col5 = st.columns(2)
        with fig_col4:
            st.markdown("### Logo Detection")
            #fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'marital')
            image = cv2.imread("../data/detected_logo/3a3878c4fa9698438884f2288bdd1ea2detected_logo.jpg")
            st.image(image)
        with fig_col5:
            st.markdown("### Edge detection")
            image = cv2.imread("../data/detected_edges/3a3878c4fa9698438884f2288bdd1ea2detected_edge.jpg")
            st.image(image)
        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)