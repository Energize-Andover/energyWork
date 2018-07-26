import pandas as pd

# Import the CSV file
# Skip the weird footer that might make this program fail
file = pd.read_csv('2018 Q1Q2 - AHS CO2 (0800-1530).csv', skipfooter=3)

# Within the series of the means, print all that are greater than 1000
print(file.mean()[file.mean() >= 1000])


