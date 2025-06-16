import pandas as pd
import streamlit as st
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

#Reading the data from excel file

df= pd.read_excel('Adidas.xlsx')
st.set_page_config(layout='wide')
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)
image = Image.open('adidas-logo.jpg')

col1, col2 = st.columns([0.1, 0.9], border = True)
with col1:
    st.image(image,width=100)

html_title = """
<style>
    .title-test {
    font-weight: bold;
    padding: 5px;
    border-radius: 6px
    }
</style>
<center><h1 class = "title-test">Adidas Interactive Sales Dashboard</h1></center>
"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1, 0.45, 0.45])

with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_date}")

with col4:
    fig = px.bar(df, x = "Retailer", y = "TotalSales", labels = {"TotalSales" : "Total Sales {$}"},
                 title = "Total Sales by Retailer", hover_data=["TotalSales"],
                 template = "gridon", height = 500)
    st.plotly_chart(fig, use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])
with view1:
    expander = st.expander("Sales by Retailer Data")
    data = df[["Retailer", "TotalSales"]].groupby(by="Retailer")["TotalSales"].sum().sort_values(ascending = False)
    expander.write(data)

with dwn1:
    st.download_button("Download Sales by Retailer", data = data.to_csv().encode("utf-8"),
                       file_name = "RetailerSales.csv", mime="text/csv")