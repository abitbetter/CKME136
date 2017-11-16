#sum all of the features found in the chicago.txt restaurants to help determine the most prevelant ones
from collections import Counter
ctr = Counter()

#sum the restaurant features from the chicago.txt dataset into a key, value pair list
with open('chicago.txt','r') as file_handle:
   for line in file_handle:
       line_words = line.strip().split() #strip removes trailing and leading whitespace as default arg, split splits the string base on whitespace as default arg
       for word in line_words:
       		if word.isnumeric() and len(word) == 3:
           		ctr[word] += 1

#stream through the features.txt list and update the key, value pairs from above with the actual description (instead of the feature code)
with open('features.txt','r') as features_file_handle:
   for line in features_file_handle:
       line_words = line.strip().split()
       if ctr[line[:3]] != 0:
       		ctr[line[4:-1]] = ctr[line[:3]]
       		del ctr[line[:3]]

#save the list into a new text file
new_file = open('feature_sum_text.txt', 'w')
new_file.write('\n'.join(map(str, ctr.most_common())))
new_file.close()
# print(ctr.most_common()) #this sorts the counter key, value pairs in desc order as a LIST!
# print(str(ctr.most_common()).strip('[]')) #this prints the key value pair as a STRING

#this is how to 'change' a key name
ctr['key change'] = ctr['249']
del ctr['249']

# print('\n'.join(map(str, ctr.most_common())))
