import requests
import math
import pandas as pd
# request = requests.get("http://10.12.4.98:8000/?facility=ahs&instance=3011595")
# print(request.content)

wing = 'A'
floor = 1

ahs_csv = pd.read_csv('../csv/ahs_air_wing.csv', na_filter=False, comment='#')

# s1 = "ahs_csv['Wing'] == " + wing
# s2 = "ahs_csv['Floor'] == " + str(floor)

df_focus = ahs_csv[(ahs_csv['Wing'] == wing) & (ahs_csv['Floor'] == str(floor))]
print(df_focus)