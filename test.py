import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.stoggle import stoggle
import jalali_pandas
import plotly.express as px
from preprocessing import convert_gregorian_to_jalali

df = pd.read_csv("total.csv")
df = convert_gregorian_to_jalali(df)

months_dict = {
    "فروردین": 1,
    "اردیبهشت": 2,
    "خرداد": 3,
    "تیر": 4,
    "مرداد": 5,
    "شهریور": 6,
    "مهر": 7,
    "آبان": 8,
    "آذر": 9,
    "دی": 10,
    "بهمن": 11,
    "اسفند": 12
}

unique_month = df['jdate'].apply(lambda x: x.split("-")[1]).unique()
month_array = []
# Get months in dataframes
for month in unique_month:
    month_array.append(list(months_dict.keys())[list(months_dict.values()).index(int(month))])

month = st.selectbox(
    'Select a date from the data:calendar::',
    month_array)

days = st.selectbox(
    'Select a date from the data:calendar::',
    df[df['jdate'].apply(lambda x: x.split("-")[1]) == int(months_dict[month])]['jdate'],
)

st.write(f'Hello, *{months_dict[month]}!* :sunglasses:')
df_temp = df[df['jdate'].apply(lambda x: x.split("-")[1]) == str(months_dict[month])]

#df[df['jdate'].apply(lambda x: x.split("-")[1]) == str(months_dict[month])]['jdate']

df_temp["jdate"] = df_temp["jdate"].str.replace("-", "/")
df_temp
# Show Barchart
fig = px.bar(df_temp,
             x='jdate',
             y=["Yac", "Ydc"],
             barmode='group',
             height=400,
             width=800,
             )

# Plot using Streamlit
st.plotly_chart(fig)

















