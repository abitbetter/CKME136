import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

data = pd.read_csv('chicago_with_features.txt', header=None, delimiter='\t')
data.columns = ["ID", "Features"]

#add new row to pandas dataframe(this is how i am adding the 'input' data at this point)
data.loc[676] = [676, 'Good Food Good Service Good Decor below $15']

# print(data.tail())
# print(data[675])

#compute the results using tdidf and cosine similarity
tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(data['Features'])
# tfidf_matrix = tf.fit_transform(data['Features'][0:2])
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}

for idx, row in data.iterrows():
# for idx, row in data[0:2].iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-676:-1]
    similar_items = [(cosine_similarities[idx][i], data['ID'][i]) for i in similar_indices]
    # print(similar_items)
    # First item is the item itself, so remove it.
    # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, item_id)
    results[row['ID']] = similar_items[1:]
    # print(results)

#get a friendly item name from the feature field, given an item ID
def item(id):
    return data.loc[data['ID'] == id]['Features'].tolist()[0].split(' - ')[0]

#reads the results out of the dictionary
def recommend(item_id, num):
    print("Recommending " + str(num) + " products similar to " + item(item_id) + " ... " + str(item_id))
    print("-------")
    recs = results[item_id][:num]
    for rec in recs:
        print("Recommended: " + item(rec[1]) + " (score:" + str(rec[0]) + ")")
        print(rec)

recommend(132, 3)
# recommend(676,5)

# print(data['Features'][1:3])

# temp = results[1][:1]
# print(str(temp[0][0]))
# print(results)

# temp = [x[0] for x in results[0]]

# print(temp)