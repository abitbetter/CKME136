#converts chicago.txt to a sparce dataframe with 0 if the feature does not exist and the feature code if it does

import pandas as pd

data = pd.read_csv("chicago.txt", sep='\t', header=None)
data.columns = ["ID", "Restaurant_Name", "Features"]

print(data.Restaurant_Name)
print(data.iloc[0,0])

#prepare columns array for the df
columnsList = ['ID', 'RN']
columnsListTail = list(range(0,257))
columns = columnsList + columnsListTail

#create dataframe with our desired header
df = pd.DataFrame(columns=columns)
print(df.head())
print(df.columns[0])

rowCount = 0

#take original chicago.txt file and put into a normalized dataframe with column headings corresponding to feature id(3 digit number) and 1 for existing in a given
#restaurant and a 0 if it does not exit.
with open('chicago.txt','r') as file_handle:
	for line in file_handle:
		line_words = line.strip().split()
		for word in line_words:
			for index in range(0,256):
				#the 'word' must be a numeric 3 digit number (ie the feature code for the restauraut)
				if word.isnumeric() and df.columns[index] == int(word) and len(word) == 3: 
					df.at[rowCount,df.columns[index]] = int(word)
				#insert the rowCount as the ID as the text file is traversed
				elif df.columns[index] == "ID":
					df.at[rowCount,df.columns[0]] = rowCount
		rowCount+=1

#add restaurant names to dataframe
rowCount = 0
with open('chicago.txt','r') as file_handle:
	for line in file_handle:
		ls = line.split('\t')
		df.at[rowCount,df.columns[1]] = ls[1]
		rowCount+=1

#fill in all NaN value in the dataframe with zeros
df.fillna(0, inplace=True)

#save dataframe to textfile using tab as delimeter
df.to_csv(r'chicago_dataframe.txt', index=None, sep='\t', mode='w')