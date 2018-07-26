# Track energy usage of the Collins Center nightly (23:00 to 4:00) between years
import pandas as pd

df2016 = pd.read_csv('Data/2016 Q1Q4 - Electrical Nightly (2300-0400).csv', skipfooter=3, engine='python', header=1)
df2017 = pd.read_csv('Data/2017 Q1Q4 - Electrical Energy & Gas Nightly (2300 - 0400).csv', skipfooter=3,
                     engine='python', header=1)
df2018 = pd.read_csv('Data/2018 Q1Q2 - AHS Electricity Gas & OA-T.csv', skipfooter=3, engine='python', header=1)

# Get data for Collins Center per year
cc2016 = df2016['HS CC (kWh)']
cc2017 = df2017['HS CC (kWh)']

# This is daily
cc2018 = df2018['HS CC Collins Center (kWh)']

print('Total CC Energy Used in 2016 -', cc2016.sum())
print('Total CC Energy Used in 2017 -', cc2017.sum())
print('Total CC Energy Used in 2018 -', cc2018.sum())
if cc2016.sum() > cc2017.sum():
    print('More energy was used at night in the Collins Center in 2016 than in 2017')
elif cc2017.sum() > cc2016.sum():
    print('More energy was used at night in the Collins Center in 2017 than in 2016')

# df2018 = pd.read_csv()
# print(df2016)
# print(df2017)

