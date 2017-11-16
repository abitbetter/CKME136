#count the individual restaurants from the user sessions to determine what the 'most popular' restaurants are
from collections import Counter
ctr = Counter()

result = {}

def counterFromList(fileName):
  with open(fileName,'r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split('\t')
       features = line_words[2].strip().split()
       result[line_words[0]] = features[:-1]
       
#this is the complete list of session data
counterFromList('session/session.1996-Q3')
counterFromList('session/session.1996-Q4')
counterFromList('session/session.1997-Q1')
counterFromList('session/session.1997-Q2')
counterFromList('session/session.1997-Q3')
counterFromList('session/session.1997-Q4')
counterFromList('session/session.1998-Q1')
counterFromList('session/session.1998-Q2')
counterFromList('session/session.1998-Q3')
counterFromList('session/session.1998-Q4')
counterFromList('session/session.1999-Q1')
counterFromList('session/session.1999-Q2')

		
#save the list into a new text file
new_file = open('session_sum_testing.txt', 'w')
new_file.write('\n'.join(map(str, ctr.most_common()))) #this will convert the list into a string and join with new line(ie a line break between each key, value pair)
new_file.close()