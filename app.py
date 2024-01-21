import streamlit as st
import pandas as pd
import plotly.express as px
from preprocessing import convert_gregorian_to_jalali

# page layout
st.set_page_config(page_title="BT2 Dashboard", page_icon="🌎", layout="centered")
st.header("Balintech Solar Panel Production", divider='grey')

# Read CSV files and Preprocessing
df = pd.read_csv("total.csv")
df = convert_gregorian_to_jalali(df)

df_weather = pd.read_csv("weather_data.csv")
df_weather = df_weather.rename(columns={'datetime': 'date'})
df_weather = convert_gregorian_to_jalali(df_weather)

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

# Month SelectBox
unique_month = df['jdate'].apply(lambda x: x.split("-")[1]).unique()
month_array = []
# Get months in dataframes
for month in unique_month:
    month_array.append(list(months_dict.keys())[list(months_dict.values()).index(int(month))])

month = st.selectbox(
    'Select a date from the data:calendar::',
    month_array)

df_bar_chart = df[df['jdate'].apply(lambda x: x.split("-")[1]) == str(months_dict[month])]
df_bar_chart["jdate"] = df_bar_chart["jdate"].str.replace("-", "/")

# Show Barchart
fig = px.bar(df_bar_chart,
             x="jdate",
             y=["Yac", "Ydc"],
             barmode='group',
             height=400,
             width=800,
labels={
                     "jdate": "date",
                     "value": "Energy, kWh",
                 },
             )
st.plotly_chart(fig)



###########################################################
# Row #1
col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        max_ac = df_bar_chart['Yac'].max()
        st.write(f"Max AC Generated in this month :top: : {max_ac:.2f} Kw/h")
with col2:
    with st.container(border=True):
        sum_ac = df_bar_chart['Yac'].sum()
        st.write(f"Total AC Generated of month :clipboard: : {sum_ac:.2f} Kw/h")

# Row #2
col3, col4 = st.columns(2)
# df_weather['date'] = df_weather['date'].str.replace("/", "-")
df_weather = convert_gregorian_to_jalali(df_weather)
with col3:
    with st.container(border=True):
        max_dc = df_bar_chart['Ydc'].max()
        st.write(f"Max DC Generated in this month :top: : {max_dc:.2f} Kw/h")
with col4:
    with st.container(border=True):
        sum_ac = df_bar_chart['Ydc'].sum()
        st.write(f"Total DC Generated of month :clipboard: : {sum_ac:.2f} Kw/h")

st.divider()

option = st.selectbox(
    'Select a date from the data:calendar::',
    df_weather[df_weather['jdate'].apply(lambda x: x.split("-")[1]) == str(months_dict[month])]['jdate'],
)

# Row B
left_column, middle_column1, middle_column2, right_column = st.columns(4)
with left_column:
    with st.container(border=True):
        st.metric(label="Maximum Temp:arrow_up_small:", value=df_weather[df_weather['jdate'] == option]['tempmax'])
with middle_column1:
    with st.container(border=True):
        st.metric("Minimum Temp:arrow_down_small:", df_weather[df_weather['jdate'] == option]['tempmin'])
with middle_column2:
    with st.container(border=True):
        st.metric("Temperature:thermometer:", str(df_weather[df_weather['jdate'] == option]['temp'].iloc[0]))
with right_column:
    with st.container(border=True):
        st.metric("Cloud Cover:sun_small_cloud:", df_weather[df_weather['jdate'] == option]['cloudcover'])

# ***********************************************************************************************************#
# Row C
left_column2, middle_column2_1, middle_column2_2, right_column2 = st.columns(4)
with left_column2:
    with st.container(border=True):
        st.metric("Sunrise:sunrise:",
                  str(df_weather[df_weather['jdate'] == option]['sunrise'].iloc[0].split(' ')[0].split("T")[1]))
with middle_column2_1:
    with st.container(border=True):
        st.metric("Sunset:sunrise_over_mountains:",
                  str(df_weather[df_weather['jdate'] == option]['sunset'].iloc[0].split(' ')[0].split("T")[1]))

with middle_column2_2:
    with st.container(border=True):
        st.metric("Solar Energy", df_weather[df_weather['jdate'] == option]['solarenergy'])
with right_column2:
    with st.container(border=True):
        st.metric("Solar Radiation", df_weather[df_weather['jdate'] == option]['solarradiation'])



# ***********************************************************************************************************#

# Row C

left_column3, right_column3 = st.columns(2)
with left_column3:
    with st.container(border=True):
        st.metric("Condition:sleuth_or_spy:",
                  str(df_weather[df_weather['jdate'] == option]['conditions'].iloc[0])
                  )
with right_column3:
    left_column_inner, right_column_inner = st.columns(2)
    with left_column_inner:
        with st.container(border=True):
            st.metric("AC generated", f"{df[df['jdate'] == option]['Ydc'].iloc[0]:.2f}")
    with right_column_inner:
        with st.container(border=True):
            st.metric("DC generated", f"{df[df['jdate'] == option]['Yac'].iloc[0]:.2f}")

st.divider()
# ***********************************************************************************************************#

# Row D
sum_ydc = df['Ydc'].sum()
sum_yac = df['Yac'].sum()
st.markdown("Total DC and AC generated up to this moment")
left_column_last, right_column_last = st.columns(2)
with left_column_last:
    with st.container(border=True):
        st.metric("AC:zap:",
                  f" {sum_yac:.2f} Kw")

with right_column_last:
    with st.container(border=True):
        st.metric("DC:zap:",
                  f" {sum_ydc:.2f} Kw")



