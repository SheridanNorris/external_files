# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 10:02:01 2020

@author: sheri
"""


import seaborn as sns
import requests
import urllib3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


#Retrieve data frpm Strava

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

activities_url = "https://www.strava.com/api/v3/athlete/activities"
auth_url = "https://www.strava.com/oauth/token"
payload = {
        'client_id': "###",
        'client_secret': '####',
        'refresh_token': '####',
        'grant_type' : "refresh_token",
        'f': 'json'
        }

res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

#print("Access Token = {}\n".format(access_token))


header = {'Authorization': 'Bearer '+ access_token}
params = {'per_page': 100, 'page':1}
my_dataset = requests.get(activities_url, headers=header, params=params).json()


#Now parse data. I'll start with Miles and Time over a 4 week period

upload = []
start_date = []
distance = []
moving_time = []
kilojoules = []

for i in range(len(my_dataset)):
    upload.append(my_dataset[i]['upload_id']) 
df1 = pd.DataFrame(upload,columns=['Upload_ID'])
    
for i in range(len(my_dataset)):    
    start_date.append(my_dataset[i]['start_date']) 
df2 = pd.DataFrame(start_date,columns=['Start_Date'])


for i in range(len(my_dataset)):    
    distance.append(my_dataset[i]['distance']) 
df3 = pd.DataFrame(distance,columns=['Distance'])
    
for i in range(len(my_dataset)):     
    moving_time.append(my_dataset[i]['moving_time']) 
df4 = pd.DataFrame(moving_time,columns=['Moving_Time'])

for i in range(len(my_dataset)):
    try:
        kilojoules.append(my_dataset[i]['kilojoules']) 
    except:
        0
df5 = pd.DataFrame(kilojoules,columns=["Kilojoules"])


final_df = pd.concat([df1, df2, df3, df4, df5], axis=1)

#Convert to Useful Measures
final_df.Distance = (final_df.Distance/1000)*0.621371
final_df.Moving_Time = (final_df.Moving_Time/60)/60
final_df.Start_Date = pd.to_datetime(final_df.Start_Date)


#Split out date parts
final_df['Year']= final_df['Start_Date'].dt.year
final_df['Month']= final_df['Start_Date'].dt.month
final_df['Week_Day']= final_df['Start_Date'].dt.dayofweek
final_df['Day']= final_df['Start_Date'].dt.day
final_df['Week'] = final_df['Start_Date'].dt.week


final_df['Start_Date'] = pd.to_datetime(final_df['Start_Date']).dt.date

# =============================================================================
# #final_df.to_excel("ride_data_1.xlsx")  
# 
# #need only week, distance and time
# plot_df = final_df[['Day','Week_Day','Week','Month', 'Year', 'Distance', 'Moving_Time', "KJ's"]]
# 
# plot_agg_df = plot_df.groupby(['Day','Week_Day','Week','Month', 'Year']).agg({'Moving_Time':'sum'})
# plot_agg_df = plot_agg_df.reset_index()
# 
# plot_agg_df = plot_agg_df.sort_values(by=['Year', 'Month', 'Week','Week_Day','Day'])
# 
# #Transpose DF and create a new row for each week
# 
# 
# plot_agg_df = pd.pivot_table(plot_agg_df, values='Moving_Time', index=['Year',  'Week'],
#                     columns=['Week_Day'], aggfunc=np.sum)
# 
# month1 = input("Enter numeric baseline month: ")
# month2 = input("Enter numeric compare month: ")
# 
# =============================================================================

may_df = final_df[final_df['Month'] == 7] 
may_df = may_df.set_index('Day')
may_df = may_df.sort_index(ascending=True)
may_df['Cum_Time'] = may_df['Kilojoules'].cumsum()


june_df = final_df[final_df['Month'] == 8] 
june_df = june_df.set_index('Day')
june_df = june_df.sort_index(ascending=True)
june_df['Cum_Time'] = june_df['Kilojoules'].cumsum()

os.chdir("C:/Users/sheri/Documents/cycling")


sns.set(rc={'figure.figsize':(8, 4)})
may = may_df['Cum_Time'].plot(linewidth=1, color = 'red', label = "July")
june = june_df['Cum_Time'].plot(linewidth=1, color = 'green', label = "August")
plt.xlabel('Day of the Month')
plt.ylabel('Hours Ridden')
plt.legend(loc="upper left")
plt.savefig('KJs July vs. August.png')


