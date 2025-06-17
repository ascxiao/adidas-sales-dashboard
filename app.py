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
    data = df[["Retailer", "TotalSales"]].groupby("Retailer")["TotalSales"].sum().sort_values(ascending = False)
    expander.write(data)

with dwn1:
    st.download_button("Download Sales by Retailer", data = data.to_csv().encode("utf-8"),
                       file_name = "RetailerSales.csv", mime="text/csv")
    

df["Month_year"] = df['InvoiceDate'].dt.strftime('%b %Y')
result = df.groupby('Month_year')['TotalSales'].sum().reset_index()

with col5:
    fig1 = px.line(result, x = 'Month_year', y = 'TotalSales', title = 'Title Sales Over Time', template = 'gridon')
    st.plotly_chart(fig1, use_container_width = True)

with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)

with dwn2:
    st.download_button("Download Monthly Sales", data = data.to_csv().encode("utf-8"),
                       file_name = "MonthlySales.csv", mime="text/csv")
st.divider()

result1 = df.groupby('State')[['TotalSales', 'UnitsSold']].sum().reset_index()

#Add the Units Sold as a line chart on a secondary y - axis

fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1["State"], y=result1["TotalSales"], name = "Total Sales"))
fig3.add_trace(go.Scatter(x=result1["State"], y=result1["UnitsSold"], mode = "lines", name = "Units Sold", yaxis='y2'))
fig3.update_layout(
    title = "Total Sales and Units Sold by State",
    xaxis = dict(title="State"),
    yaxis = dict(title = "Total Sales", showgrid = False),
    yaxis2 = dict(title="Units Sold", overlaying = "y", side = "right"),
    template = "gridon",
    legend = dict(x=1, y=1.1)
)

_, col6 = st.columns([0.1, 1])
with col6:
    st.plotly_chart(fig3, use_container_width= True)

_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])

with view3:
    expander = st.expander("View Data Sales by Units Sold")
    expander.write(result1)
with dwn3:
    st.download_button("Get Data", data=result.to_csv().encode("utf-8"),
                       file_name = "Sales_by_UnitsSold.csv", mime="text/csv")
st.divider()

_, col7 = st.columns =([0.1, 1])
treemap = df[['Region', 'City', 'TotalSales']].hroupby(by = ['Region', 'City'])['TotalSales']

fig4 = px.treemap(treemap, path = ['Region',])