import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency # type: ignore
import streamlit as st # type: ignore

sns.set(style='dark')

def get_total_count_by_day_df(day_df):
   day_count_df = day_df.groupby(by="one_of_week").agg({"cnt": ["sum"]})
   return day_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day_df):
   regis_df =  day_df.groupby(by="dteday").agg({
      "registered": "sum"
    })
   regis_df = regis_df.reset_index()
   regis_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return regis_df

def total_casual_df(day_df):
   casual_df =  day_df.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   casual_df = casual_df.reset_index()
   casual_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return casual_df

def sum_order (day_df):
    sum_order_items_df = day_df.groupby(by="one_of_week").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def various_season (day_df): 
    season_df = day_df.groupby(by="season").cnt.sum().reset_index() 
    return season_df

hours_df = pd.read_csv("hour_data.csv")
days_df = pd.read_csv("day_data.csv")

datetime_columns = ["dteday"]
hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)

for column in datetime_columns:
   hours_df[column] = pd.to_datetime(hours_df[column])
   days_df[column] = pd.to_datetime(days_df[column])


min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

with st.sidebar:
   st.image("https://miro.medium.com/v2/resize:fit:1100/format:webp/1*tFONSoZiVSpQGP_s1BvfJg.jpeg")


   start_date, end_date = st.date_input(
      label='Rentang Waktu',
      min_value=min_date_days,
      max_value=max_date_days,
      value=[min_date_days, max_date_days])
   
main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) &
                          (hours_df["dteday"] >= str(end_date))]

main_df_day = days_df[(days_df["dteday"] >= str(start_date)) &
                        (days_df["dteday"] >= str(end_date))]

day_count_df = get_total_count_by_day_df(main_df_day)
days_df_count_2011 = count_by_day_df(main_df_day)
regis_df = total_registered_df(main_df_day)
casual_df = total_casual_df(main_df_day)
sum_order_items_df = sum_order(main_df_day)
season_df = various_season(main_df_hour)


st.header('Bike Sharing Dashboard :bike:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)

with col1:
   total_rents = days_df_count_2011.cnt.sum()
   st.metric("Total Sharing Bike", value=total_rents)

with col2:
   total_sum = casual_df.casual_sum.sum()
   st.metric("Total Casual", value=total_sum)

with col3:
   total_sum = regis_df.register_sum.sum()
   st.metric("Total Registered", value=total_sum)

st.subheader("Performa penyewaan sepeda dalam beberapa tahun terakhir")

fig, ax = plt.subplots(figsize=(25, 5))
ax.plot(
   days_df["dteday"],
   days_df["cnt"],
   marker='o',
   linewidth=2,
   color="#578FCA"
)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("The Impact of Seasons on Bicycle Rental Trends")
labels = 'Spring', 'Summer', 'Fall', 'Winter'
sizes = [14.3, 27.9, 32.2, 25.6]
explode = (0, 0, 0.1, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels,  autopct='%1.1f%%', colors=["#BC9F8B", "#B5CFB7", "#CADABF", "#E7E8D8"], 
        shadow=False, startangle=90)
ax1.axis('equal')

st.pyplot(fig1)

st.subheader("The Most and Least Rented Days")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#4A628A", "#7AB2D3","#7AB2D3", "#7AB2D3", "#7AB2D3", "#7AB2D3", "#7AB2D3"]

sns.barplot(x="one_of_week", y="cnt", data=sum_order_items_df.head(7), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Day", fontsize=30)
ax[0].set_title("The Most Rented Days", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=20)

sns.barplot(x="one_of_week", y="cnt", data=sum_order_items_df.sort_values(by="one_of_week", ascending=True).head(7), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Day", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("The Least Rented Days", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=20)

st.pyplot(fig)
