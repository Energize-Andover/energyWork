import pandas as pd

df = pd.read_csv('2018 Q1Q2 - AHS Temprature (0730-1500 hrs).csv.csv', skipfooter=3, engine='python')
# print(df.head())
# Filters data to just be weekdays
weekdays = df[pd.to_datetime(df['Unnamed: 0']).dt.weekday < 5]

# Filters data to be between 8 and 15 o'clock
weekdaysTime = weekdays[(pd.to_datetime(weekdays['Unnamed: 0']).dt.hour >= 8) &
                        (pd.to_datetime(weekdays['Unnamed: 0']).dt.hour <= 15)]

# Filters data to be in June
inJune = weekdaysTime[(pd.to_datetime(weekdaysTime['Unnamed: 0'])).dt.month == 6]

# Finds the average temp of the filtered data
avgTemp = inJune.mean()

# Prints all the data where the average temp is greater than 75 deg
print(avgTemp[avgTemp >= 75])
