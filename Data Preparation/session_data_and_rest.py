result = {}

def counterFromList(fileName):
  with open(fileName,'r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split('\t')
       result[line_words[0].replace(':',' ',1)] = line_words[-1]
         

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

# print(result)
#stream from the chicago.txt list and update the key, value pairs from above with the actual description (instead of the restaurant code)
new_file = open('session_date_and_rest.txt', 'w')
# new_file.write('\n'.join(map(str, ctr.most_common()))) #this will convert the list into a string and join with new line(ie a line break between each key, value pair)

for key, val in result.items():
  new_file.write(str(key+'\t'+val) + '\n')
new_file.close()