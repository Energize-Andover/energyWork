import pandas as pd

# Import the CSV file
# Index_col shifts over the index column to the column with the dates
df = pd.read_csv('2018 Q1Q2 - AHS CO2 (0800-1530).csv', index_col=0)

# Create new dataframes that each isolate one specific day
mon = df.filter(like='Mon', axis=0)
tues = df.filter(like='Tues', axis=0)
wed = df.filter(like='Wed', axis=0)
thur = df.filter(like='Thurs', axis=0)
fri = df.filter(like='Fri', axis=0)

# Concatenate all the days back into
weekdays = pd.concat([mon, tues, wed, thur, fri])

# Find the average CO2 levels of each day and then find all that average over 1000 ppm
result = weekdays.mean()[weekdays.mean() >= 1000]

# Print the result
print(result)
