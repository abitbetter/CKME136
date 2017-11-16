import re #regex library
from collections import Counter
ctr = Counter()

#THESE SHOULD BE A FUNCTION TO RECUDE CODE REPITITION!!!

#sum the seesion from the chicago.txt dataset into a key, value pair list
with open('session/session.1996-Q3','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

with open('session/session.1996-Q4','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

with open('session/session.1997-Q1','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

with open('session/session.1997-Q2','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

with open('session/session.1997-Q3','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

with open('session/session.1997-Q4','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

with open('session/session.1998-Q1','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

with open('session/session.1998-Q2','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

with open('session/session.1998-Q3','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

with open('session/session.1998-Q4','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

with open('session/session.1999-Q1','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

with open('session/session.1999-Q2','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split()
       if len(line_words[-1]) == 2:
        line_words[-1] = "0" + line_words[-1]
       if len(line_words[-1]) == 1:
        line_words[-1] = "00" + line_words[-1]
       ctr[line_words[-1]] += 1 #last word of the line_words list of words

#stream from the chicago.txt list and update the key, value pairs from above with the actual description (instead of the restaurant code)
with open('chicago.txt','r') as features_file_handle:
    for line in features_file_handle:
      match = re.search("([a-zA-Z\s!'&-.]+)", line) #this regex needs some fine tuning
      ctr[match.group(0).strip()] = ctr[line[4:7]]
      del ctr[line[4:7]]
		
#save the list into a new text file
new_file = open('session_sum_text.txt', 'w')
new_file.write('\n'.join(map(str, ctr.most_common())))
new_file.close()