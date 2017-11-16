import pandas as pd
import datetime

df = pd.read_csv("session_date_and_rest.txt", sep='\t', header=None)
df.columns = ["date", "Restaurant_ID"]

def ourDatetime(day, month, year):
   now = datetime.datetime.now()
   return now.replace(day=day, month=month, year=year) 

#convert datetime to datetime data type in the dataframe
df['date'] = pd.to_datetime(df['date'])

# print(df) #date in df is correct at this point

#breakfast, lunch, dinner dataframes (will not be include late night restaurants/bars)
columns = ['date', 'Restaurant_ID']
df_winter = pd.DataFrame(columns=columns) 	# summer -- May-Oct
df_summer = pd.DataFrame(columns=columns)	# winter -- Nov-Apr

# Loop over the df and compare time -- save the separate df's into various dataframes
for index, row in df.iterrows():
	#this will remove all rows that have -1 as restaurant id (meaning the use did not choose)
	if(row['Restaurant_ID'] == -1):
		continue
		print("found -1")
	if(row['date'].month > ourDatetime(1,4,1999).month and row['date'].month < ourDatetime(1,11,1999).month): #summer
		df_summer.at[index, 'date'] = row['date']
		df_summer.at[index, 'Restaurant_ID'] = row['Restaurant_ID']
	else: #winter
		df_winter.at[index, 'date'] = row['date']
		df_winter.at[index, 'Restaurant_ID'] = row['Restaurant_ID']

#save dataframe to textfile for quicker processing and analysis
df_summer.to_csv(r'session_summer.txt', index=None, sep='\t', mode='w', header=True)
df_winter.to_csv(r'session_winter.txt', index=None, sep='\t', mode='w', header=True)

# print(ourDatetime(1, 5, 1999).month)