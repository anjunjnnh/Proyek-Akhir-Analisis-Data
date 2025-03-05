import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st # type: ignore
from babel.numbers import format_currency # type: ignore
sns.set(style='dark')

def get_total_count_by_hour_df(hour_df):
  hour_count_df =  hour_df.groupby(by="hours").agg({"cnt": ["sum"]})
  return hour_count_df

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

hour_df = pd.read_csv("all_data.csv")
day_df = pd.read_csv("day_data.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date_day = day_df["dteday"].min()
max_date_day = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://miro.medium.com/v2/resize:fit:1100/format:webp/1*tFONSoZiVSpQGP_s1BvfJg.jpeg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_day,
        max_value=max_date_day,
        value=[min_date_day, max_date_day])
  
main_df_hour = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                        (hour_df["dteday"] <= str(end_date))]

main_df_day = day_df[(day_df["dteday"] >= str(start_date)) & 
                     (day_df["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_day)
regis_df = total_registered_df(main_df_day)
casual_df = total_casual_df(main_df_day)

st.header('Bike Sharing :bike: :sparkles:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.cnt.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = regis_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = casual_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)


st.subheader("Company Sales Performance in Recent Years")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    day_df["dteday"],
    day_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='x', labelsize=10)  
ax.tick_params(axis='y', labelsize=10)  
st.pyplot(fig)

st.subheader("Total Users by Hour")

plt.figure(figsize=(35, 15))
sns.lineplot(data=hour_df, x='hours', y='cnt', color='blue')
plt.xlabel('Hour', fontsize=30)
plt.ylabel('Number of Rider', fontsize=30)
plt.title('Total Users by Hour', fontsize=35)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)

st.pyplot(plt)

st.subheader("Influence of Temperature and Humidity")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(data=hour_df, x='temp2_binned', y='cnt', palette=['#EFDCAB', '#EFDCAB', '#D8D2C2'], ax=ax[0])
ax[0].set_title('Total Users by Temperature', fontsize=35)
ax[0].set_xlabel('Weather', fontsize=30)
ax[0].set_ylabel('Total Users', fontsize=30)
ax[0].tick_params(axis='both', labelsize=25)

sns.barplot(data=hour_df, x='hum2_binned', y='cnt', palette=['#D8D2C2', '#EFDCAB', '#EFDCAB'], ax=ax[1])
ax[1].set_title('Total Users by Humidity', fontsize=35)
ax[1].set_xlabel('Humidity', fontsize=30)
ax[1].set_ylabel('Total Users', fontsize=30)
ax[1].tick_params(axis='both', labelsize=25)
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].invert_xaxis()

st.pyplot(fig)