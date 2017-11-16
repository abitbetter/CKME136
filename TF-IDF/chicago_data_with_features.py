import csv

#convert features.txt to dictionary with key value pairs
with open("features.txt",'r') as f:
   for line in f:
       d = dict(line.strip().split(None,1) for line in f) #split(None,1) - no delimeter(whitespace by default) and split the line only once


print(d)

result = {}
featuresString = ""

#convert the chicage.txt data to key value pairs with id as key and desription as value
with open('chicago.txt','r') as file_handle:
  for line in file_handle:
    line_words = line.strip().split('\t',2) #strip removes trailing and leading whitespace as default arg, split splits the string base on whitespace as default arg
    features = line_words[2].split()
    for code in features:
      featuresString = featuresString + d[str(code)] + " "
    result[line_words[0]] = featuresString
    featuresString = ""

# print(result)

new_file = open('chicago_with_features.txt', 'w')
# new_file.write('\n'.join(map(str, ctr.most_common()))) #this will convert the list into a string and join with new line(ie a line break between each key, value pair)

for key, val in result.items():
  new_file.write(str(key+'\t'+val) + '\n')
new_file.close()