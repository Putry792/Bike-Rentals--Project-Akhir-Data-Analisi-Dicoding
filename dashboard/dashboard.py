import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


sns.set(style='dark')

# read dataset
days_df = pd.read_csv('dashboard/days_df.csv')

# create_daily_rent_df digunakan untuk menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby('dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# create_casual_df digunakan untuk menyiapkan casual_df
def create_casual_df(df):
    daily_casual_df = df.groupby('dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_df

# create_registered_df digunakan untuk menyiapkan registered_df
def create_registered_df(df):
    registered_df = df.groupby('dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_df

# create_season_df digunakan untuk meyiapkan season_df
def create_season_df(df):
    season_df = df.groupby('season')[['casual', 'registered']].sum().reset_index()
    return season_df

# create_monthly_rent_df digunakan untuk menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby('month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# create_weekday_rent_df digunakan untuk menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby('weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# create_workingday_rent_df digunakan untuk menyiapkan working_rent_df
def create_working_rent_df(df):
    working_rent_df = df.groupby('workingday').agg({
        'count': 'sum'
    }).reset_index()
    return working_rent_df

# create_holiday_rent_df digunakan untuk menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby('holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# create_weathersit_df digunakan untuk menyiapkan weathersit_df
def create_weathersit_df(df):
    weathersit_df = df.groupby('weathersit').agg({
        'count': 'sum'
    }).reset_index()
   

# membuat komponen filter
min_date = pd.to_datetime(days_df['dateday']).dt.date.min()
max_date = pd.to_datetime(days_df['dateday']).dt.date.max()


# membuat sidebar
with st.sidebar:
    # menambahkan nama perusahaan
    st.header('Putry Bike Rental')
    
    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentan Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


main_df = days_df[(days_df['dateday'] >= str(start_date)) &
                  (days_df['dateday'] <= str(end_date))]


daily_rent_df = create_daily_rent_df(main_df)
daily_casual_df = create_casual_df(main_df)
registered_df = create_registered_df(main_df)
season_df = create_season_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
working_rent_df = create_working_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weathersit_df = create_weathersit_df(main_df)

st.header('Bicycle Rental Dashboard 🚴‍♂️')

# menampilkan daily rent
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_casual_df = daily_casual_df['casual'].sum()
    st.metric('Casual User', value=daily_casual_df)

with col2:
    registered_df = registered_df['registered'].sum()
    st.metric('Registered User', value=registered_df)

with col3:
    total_rent = daily_rent_df['count'].sum()
    st.metric('Total Rent', value=total_rent)

# menampilkan monthly rentals
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['count'],
    marker='o',
    linewidth=2,
)
for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel('Month')
ax.tick_params(axis='y', labelsize=25, rotation=45)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

# menampilkan seasons rentals
st.subheader('Seasons Rentals')
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=season_df,
    label='Registered',
    ax= ax, 
    color='tab:blue'
)

sns.barplot(
    x='season',
    y='casual',
    data=season_df,
    label='Casual',
    ax= ax,
    color='tab:orange'
)

for index, row in season_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)
   

ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig) 

# menampilkan weatherly rentals
st.subheader('Weatherly Rentals')
fig, ax= plt.subplots(figsize=(16, 8))

sns.barplot(
    x= 'weathersit',
    y='count',
    data=days_df,
    ax= ax,
    palette= 'bright'
)

ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig) 

# menampilkan weekday. working, and holiday rentals
st.subheader('Weekday, Workingday, and Holiday Rentals')

fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))

# Berdasarkan weekday
# Berdasarkan hari kerja(workingday)
sns.barplot(
    x='workingday',
    y='count',
    data=days_df,
    ax = ax[0],
    palette= 'bright'
   
)
ax[0].set_title('Jumlah Sewa Sepeda Berdasarkan Hari Kerja(workingday)')
ax[0].set_ylabel('Jumlah Sewa Sepeda')

# Berdasarkan hari libur (holiday)
sns.barplot(
    x='holiday',
    y='count',
    data=days_df,
    ax = ax[1],
    palette= 'bright'
)
ax[1].set_title('Jumlah Sewa Sepeda Berdasarkan Hari Libur(holiday)')
ax[1].set_ylabel('Jumlah Sewa Sepeda')

# Berdasarkan weekday
sns.barplot(
    x='weekday',
    y='count',
    data=days_df,
    ax= ax[2],
    palette= 'bright'
)
ax[2].set_title('Jumlah Sewa Sepeda Berdasarkan Weekday')
ax[2].set_ylabel('Jumlah Sewa Sepeda')

plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright (c) Putri Nur Fadillah 2023')
