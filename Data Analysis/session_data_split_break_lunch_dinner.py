import pandas as pd
import datetime

df = pd.read_csv("session_date_and_rest.txt", sep='\t', header=None)
df.columns = ["date", "Restaurant_ID"]

def ourDatetime(hr, min=0, sec=0, micros=0):
   now = datetime.datetime.now()
   return now.replace(hour=hr, minute=min, second=sec, microsecond=micros) 

#convert datetime to datetime data type in the dataframe
df['date'] = pd.to_datetime(df['date'])

# print(df) #date in df is correct at this point

#breakfast, lunch, dinner dataframes (will not be include late night restaurants/bars)
columns = ['date', 'Restaurant_ID']
df_breakfast = pd.DataFrame(columns=columns) 	# breakfast -- 4am - 11am
df_lunch = pd.DataFrame(columns=columns)		# lunch -- 11am - 4pm
df_dinner = pd.DataFrame(columns=columns)		# dinner -- 4pm - 4am

#Loop over the df and compare time -- save the separate df's into various dataframes
for index, row in df.iterrows():
	#this will remove all rows that have -1 as restaurant id (meaning the use did not choose)
	if(row['Restaurant_ID'] == -1):
		continue
		print("found -1")
	if(row['date'].time() < ourDatetime(11).time() and row['date'].time() > ourDatetime(4).time()):
		# df_before_noon[row['date']] = row['Restaurant_ID']
		df_breakfast.at[index, 'date'] = row['date']
		df_breakfast.at[index, 'Restaurant_ID'] = row['Restaurant_ID']
	elif(row['date'].time() < ourDatetime(16).time() and row['date'].time() > ourDatetime(11).time()):
		df_lunch.at[index, 'date'] = row['date']
		df_lunch.at[index, 'Restaurant_ID'] = row['Restaurant_ID']
	else:
		# df_after_noon[row['date']] = row['Restaurant_ID']
		df_dinner.at[index, 'date'] = row['date']
		df_dinner.at[index, 'Restaurant_ID'] = row['Restaurant_ID']

#save dataframe to textfile for quicker processing
df_breakfast.to_csv(r'session_breakfast.txt', index=None, sep='\t', mode='w', header=True)
df_lunch.to_csv(r'session_lunch.txt', index=None, sep='\t', mode='w', header=True)
df_dinner.to_csv(r'session_dinner.txt', index=None, sep='\t', mode='w', header=True)