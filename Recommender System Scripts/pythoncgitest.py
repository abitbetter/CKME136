#!C:\Users\Alex\Anaconda3\python.exe
import cgi, json
# import cgitb
# cgitb.enable() #enables error handler that displays output in web browser

print("Content-type: text/html\n\n")

form = cgi.FieldStorage()
meal = form.getvalue("meal")
price = form.getvalue("price")
decor = form.getvalue("decor")
quality = form.getvalue("quality")
service = form.getvalue("service")
season = form.getvalue("season")

result = {}

result['success'] = True
result['message'] = 'Send message about script success/failure'

d = {}
#only store value for keys that were input(if some were left empty the willed not be stores in data)
for k in form.keys():
	d[k] = form.getvalue(k)

result['data'] = d

# print(json.dumps(result)) #this prints json in string format

import pandas as pd
import numpy as np
from kmodes.kmodes import KModes

#IMPORT DATA
#load the dataframe with finalized features
df = pd.read_csv("session_new_dataframe.txt", sep='\t')

#load in chicago restaurant dataset with out text features for final reference
chicago = pd.read_csv("chicago.txt", sep='\t', header=None)
chicago.columns = ["ID", "name", "features"]

#load in chicago restaurant dataset with text features for final reference
chicago_text_features = pd.read_csv("chicago_with_features.txt", sep='\t', header=None)
chicago_text_features.columns = ["ID", "features"]

#load in chicago dataset with 1's and 0's for clustering
#x - catagorical variable from sparse chicago dataset
chicago_clustering = np.genfromtxt('chicago_dataframe_one_and_zero.txt', dtype=int, delimiter='\t', skip_header=1)[:, 2:]
#y - chicago restaurant names (usecols - 0 is the restaurant ID, 1 is the restaurant name as text)
chicago_clustering_labels = np.genfromtxt('chicago_dataframe_one_and_zero.txt', dtype=str, delimiter='\t', usecols=(0, ), skip_header=1)


#EXTRACT THE SUBSET OF DATA BASED ON USER SPECIFICATIONS
#this should be stored in an array or simply use the incoming json
season = 1
meal = 2
price = 2
decor = 2
quality = 2
service = 2
cluster_num = 3
#season(1 - summer, 0 - winter)
#time(1 - breakfast, 2 - lunch, 3 - dinner)
#price(1 - low, 2 - mid, 3 - high)
#decor(1 - low, 2 - mid, 3 - high)
#quality(1 - low, 2 - mid, 3 - high)
#service(1 - low, 2 - mid, 3 - high)

#result dataframe from initial user session subset
columns = ['date', 'Restaurant_ID', 'season', 'meal', 'price', 'decor', 'quality', 'service']
user_session_subset = pd.DataFrame(columns=columns)

#save the result in a df based on the search criteria(season, meal, price, decor, quality, service)
for index, row in df.iterrows():
	#extract the rows from the user session data that meets our criteria
	if row['season'] == season and row['meal'] == meal and row['price'] == price and row['decor'] == decor and row['quality'] == quality and row['service'] == service:
		user_session_subset.at[index] = row


#THIS WILL EXTRACT THE CHICAGO_ZERO_AND_ONE RESTAURANTS THAT MATCH WITH THE ONES FOUND FROM THE INITIAL SUBSET(required for clustering)
#get count of user session subset
user_session_subset_count = pd.crosstab(index=user_session_subset['Restaurant_ID'], columns="count")

mask = np.zeros(len(chicago_clustering), dtype=bool)
mask[user_session_subset_count['count'].index.values.astype(int)] = True

chicago_clustering_labels = chicago_clustering_labels[mask]
chicago_clustering = chicago_clustering[mask]


#CLUSTERING
#method - Huang, number of clusters - 4, verbose=1 mean textual output (0 is no output)
kmodes_huang = KModes(n_clusters=3, init='Huang', verbose=0)
kmodes_huang.fit(chicago_clustering)

#this joins the restaurant name
cluster_results = np.column_stack((chicago_clustering_labels,kmodes_huang.labels_))

#convert numpy matrix to pandas dataframe
cluster_result_df = pd.DataFrame(cluster_results)
cluster_result_df.columns = ['Restaurant', 'Cluster']


#JOIN THE CLUSTERING RESULTS WITH user_session_subset_count TO GET OUT FINAL RESULTS
#remove existing indecies so the new ones line up and df's can be joined
cluster_result_df.reset_index(drop=True, inplace=True)
user_session_subset_count.reset_index(drop=True, inplace=True)

#join the cluster results with the restaurant counts
clusters_with_counts = pd.concat( [cluster_result_df, user_session_subset_count], axis=1) 


#SELECT THE 'MOST POPULAR' RESTAURANT FROM EACH OF THE 3(or whatever) CLUSTERS
columns = ["id", "name", "features"]
final_df = pd.DataFrame(columns=columns)
for i in range(cluster_num):
	key = "cluster{0}".format(i)
	max_cluster_value = clusters_with_counts.loc[clusters_with_counts['Cluster'] == str(i)]['count'].max(axis=0)
	max_cluster_rest_id = clusters_with_counts.loc[clusters_with_counts['count'] == max_cluster_value]

	rest_name = chicago["name"].values[int(max_cluster_rest_id['Restaurant'])]
	rest_id = chicago["ID"].values[int(max_cluster_rest_id['Restaurant'])]
	rest_feat = chicago_text_features["features"].values[int(max_cluster_rest_id['Restaurant'])]

	final_df.at[i, "id"] = rest_id
	final_df.at[i, "name"] = rest_name
	final_df.at[i, "features"] = rest_feat


print(json.dumps(result))