#!C:\Users\Alex\Anaconda3\python.exe
import cgi, json
import pandas as pd
import numpy as np
from kmodes.kmodes import KModes
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

print("Content-type: text/html\n\n")

#convert html datetime to a usable python datetime
def convert_to_py_datetime(dt):
	date_processing = dt.replace('T', '-').replace(':', '-').split('-')
	date_processing = [int(v) for v in date_processing]
	return datetime.datetime(*date_processing)

def ourTime(hr, min=0, sec=0, micros=0):
   now = datetime.datetime.now()
   return now.replace(hour=hr, minute=min, second=sec, microsecond=micros)

def ourDate(day, month, year):
   now = datetime.datetime.now()
   return now.replace(day=day, month=month, year=year) 

#extract season and 'meal' from the html_datetime
def get_meal(dt):
	#breakfast
	if dt.time() < ourTime(11).time() and dt.time() > ourTime(4).time():
		meal = 1
	#lunch
	elif dt.time() < ourTime(16).time() and dt.time() > ourTime(11).time():
		meal = 2
	#dinner
	else:
		meal = 3
	return meal

#determine the season based on html_datetime
def get_season(dt):
	#summer
	if dt.month > ourDate(1,4,1999).month and dt.month < ourDate(1,11,1999).month:
		season = 1
	#winter
	else:
		season = 0
	return season

#initialize the final result dictionary
def init_result(result):	
	result['success'] = True #use a flag to check for any error thoughout the script
	result['message'] = 'Send message about script success/failure' #attach a message to the error
	#if we adjusted the user input, record in tweak / tweak_message keys
	result['tweak'] = False
	result['tweak_message'] = ''

	d = {}
	#only store value for keys that were input(if some were left empty they will not be stores in data)
	for k in form.keys():
		d[k] = form.getvalue(k)

	d['rest_id'] = 999
	result['previous_data'] = d

	result['test'] = str(meal)

	return result

#save the result in a df based on the search criteria(season, meal, price, decor, quality, service)
def find_user_subset(df, user_ratings, season, meal, print, decor, quality, service):
	for index, row in user_ratings.iterrows():
		#extract the rows from the user session data that meets our criteria
		if row['season'] == int(season) and row['meal'] == int(meal) and row['price'] == int(price) and row['decor'] == int(decor) and row['quality'] == int(quality) and row['service'] == int(service):
			df.at[index] = row
	return df
	

#if no results are found from the subset search, decrement the highest rated attributes one by one until a subset is found
def modify_user_input():
	global price, decor, quality, service
	found = False
	if 3 in (price, decor, quality, service):
		if price == 3:
			price -= 1
			result['tweak'] = True
			result['tweak_message'] = result['tweak_message'] + ' Price '
			found = True
		elif decor == 3:
			decor -= 1
			result['tweak'] = True
			result['tweak_message'] = result['tweak_message'] + ' Decor '
			found = True
		elif service == 3:
			service -= 1
			result['tweak'] = True
			result['tweak_message'] = result['tweak_message'] + ' Service '
			found = True
		elif quality == 3:
			quality -= 1
			result['tweak'] = True
			result['tweak_message'] = result['tweak_message'] + ' Quality '
			found = True
	else:
		if price == 2:
			price -= 1
			result['tweak'] = True
			result['tweak_message'] = result['tweak_message'] + ' Price '
			found = True
		elif decor == 2:
			decor -= 1
			result['tweak'] = True
			result['tweak_message'] = result['tweak_message'] + ' Decor '
			found = True
		elif service == 2:
			service -= 1
			result['tweak'] = True
			result['tweak_message'] = result['tweak_message'] + ' Service '
			found = True
		elif quality == 2:
			quality -= 1
			result['tweak'] = True
			result['tweak_message'] = result['tweak_message'] + ' Quality '
			found = True

		
#clustering
def clustering(user_session_subset, chicago_clustering, chicago_clustering_labels):
	#this will extract the chicago_zero_and_one restaurants that match with the ones found from the initial user session subset(this format is required for clustering)
	user_session_subset_count = pd.crosstab(index=user_session_subset['Restaurant_ID'], columns="count")
	mask = np.zeros(len(chicago_clustering), dtype=bool)
	mask[user_session_subset_count['count'].index.values.astype(int)] = True
	chicago_clustering_labels = chicago_clustering_labels[mask]
	chicago_clustering = chicago_clustering[mask]
m
	#method - Huang, number of clusters - 4, verbose=1 mean textual output (0 is no output), n_init - number of times the algorith runs with different centroid seed, with the best output selected from those independent runs
	#highest n_init is slower but provide more consistent results
	kmodes_huang = KModes(n_clusters=3, init='Huang', verbose=0, n_init=20)
	kmodes_huang.fit(chicago_clustering)

	#join the results to the restaurant name
	cluster_results = np.column_stack((chicago_clustering_labels,kmodes_huang.labels_))

	#convert numpy matrix to pandas dataframe
	cluster_result_df = pd.DataFrame(cluster_results)
	cluster_result_df.columns = ['Restaurant', 'Cluster']

	#join the clustering results with user_session_subset_count to get our final results
	#remove existing indecies so the new ones line up and df's can be joined
	cluster_result_df.reset_index(drop=True, inplace=True)
	user_session_subset_count.reset_index(drop=True, inplace=True)

	#join the cluster results with the restaurant counts
	clusters_with_counts = pd.concat( [cluster_result_df, user_session_subset_count], axis=1) 

	return clusters_with_counts

#select the 'most popular' restaurant from each of the 3 clusters
def get_most_popular_rest(clusters_with_counts, chicago, chicago_with_features, cluster_num):
	columns = ["id", "name", "features"]
	final_df = pd.DataFrame(columns=columns)

	for i in range(cluster_num):
		# key = "cluster{0}".format(i)
		max_cluster_value = clusters_with_counts.loc[clusters_with_counts['Cluster'] == str(i)]['count'].max(axis=0)
		max_cluster_rest_id = clusters_with_counts.loc[clusters_with_counts['count'] == max_cluster_value]

		#if there is more than one restaurant with the same max count in a cluster, pick one
		if len(max_cluster_rest_id) > 1:
			max_cluster_rest_id = max_cluster_rest_id[0:1]

		rest_name = chicago["name"].values[int(max_cluster_rest_id['Restaurant'])]
		rest_id = chicago["ID"].values[int(max_cluster_rest_id['Restaurant'])]
		rest_feat = chicago_text_features["features"].values[int(max_cluster_rest_id['Restaurant'])]

		final_df.at[i, "id"] = rest_id
		final_df.at[i, "name"] = rest_name
		final_df.at[i, "features"] = rest_feat
		final_df.at[i, "count"] = max_cluster_value

	return final_df


cluster_num = 3

#handling html POST data
form = cgi.FieldStorage()
price = int(form.getvalue("price"))
decor = int(form.getvalue("decor"))
quality = int(form.getvalue("quality"))
service = int(form.getvalue("service"))
action = str(form.getvalue('action'))
prev_recommendation = int(form.getvalue('prev_recommendation'))
html_datetime = form['datetime'].value

python_datetime = convert_to_py_datetime(html_datetime)
meal = get_meal(python_datetime)
season = get_season(python_datetime)

#initialize the result dictionary that will be used as the output json
result = {}
result = init_result(result)
result['action'] = action

#import data
user_ratings = pd.read_csv("session_new_dataframe.txt", sep='\t')
chicago = pd.read_csv("chicago.txt", sep='\t', header=None)
chicago.columns = ["ID", "name", "features"]
chicago_text_features = pd.read_csv("chicago_with_features.txt", sep='\t', header=None)
chicago_text_features.columns = ["ID", "features"]
chicago_clustering = np.genfromtxt('chicago_dataframe_one_and_zero.txt', dtype=int, delimiter='\t', skip_header=1)[:, 2:]
chicago_clustering_labels = np.genfromtxt('chicago_dataframe_one_and_zero.txt', dtype=str, delimiter='\t', usecols=(0, ), skip_header=1)

#if use selected 'submit query' this will execute
if action == 'submit':
	#find user session subset based on user input
	columns = ['date', 'Restaurant_ID', 'season', 'meal', 'price', 'decor', 'quality', 'service']
	user_session_subset = pd.DataFrame(columns=columns)
	user_session_subset = find_user_subset(user_session_subset, user_ratings, season, meal, price, decor, quality, service)
	
	#check that number of restaurants founds is larger than the number of clusters, if not tweak the search query features
	while(len(pd.crosstab(index=user_session_subset['Restaurant_ID'], columns="count")) < (cluster_num + 1)):
		modify_user_input()
		user_session_subset.drop(user_session_subset.index, inplace=True)
		user_session_subset = find_user_subset(user_session_subset, user_ratings, season, meal, price, decor, quality, service)
	
	#cluster the resulting user session subset
	clusters_with_counts = clustering(user_session_subset, chicago_clustering, chicago_clustering_labels)
	
	#determine most popular restaurants in each of the 3 clusters
	final_df = get_most_popular_rest(clusters_with_counts, chicago, chicago_text_features, cluster_num)
	final_df = final_df.sort_values("count", ascending=False)
	mydict = dict(zip(final_df.name, final_df.features))
	result['data'] = mydict

	#store id of the first choice for later use(ie in the similar restaurants option)
	first_choice_rest_id = int(final_df.iloc[0, 0])
	result['previous_data']['rest_id'] = first_choice_rest_id

	result['test'] = int(prev_recommendation)

#if use selected 'find similar restaurants' this will execute
elif action == 'similar':
	#compute the results using tdidf and cosine similarity
	tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df=0, stop_words='english')
	tfidf_matrix = tf.fit_transform(chicago_text_features['features'])
	cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

	tf_idf_scores = {}

	for idx, row in chicago_text_features.iterrows():
	    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
	    similar_items = [(cosine_similarities[idx][i], chicago_text_features['ID'][i]) for i in similar_indices]
	    # First item is the item itself, so remove it.
	    # Each dictionary entry is like: [(1,2), (3,4)], with each tuple being (score, item_id)
	    tf_idf_scores[row['ID']] = similar_items[1:]

	#extract the top 3(number of clusters/recommendations) tf-idf restaurant info for similar restaurants to previous user choice
	recs = tf_idf_scores[int(prev_recommendation)][:cluster_num]

	#format tf-idf reults and store in final_df
	columns = ["id", "name", "features", "similarity"]
	final_df = pd.DataFrame(columns=columns)
	for i, rec in enumerate(recs):
		rest_id = rec[1]
		rest_name = chicago["name"].values[rest_id]
		rest_feat = chicago_text_features["features"].values[rest_id]

		#store recommendations in final_df to be used in result json
		row = [rest_id, rest_name, rest_feat, rec[0]]
		final_df.loc[i] = row

		#store the tf-idf score in output json for display to user
		index = i + 1
		key = "rating" + str(index)
		result[key] = round(rec[0], 3)

	#store id of the first choice for later use(ie in the similar restaurants option)
	first_choice_rest_id = int(final_df.iloc[0, 0])
	result['previous_data']['rest_id'] = first_choice_rest_id

	#add final recommendations to the outgoing json
	data = dict(zip(final_df.name, final_df.features))
	result['data'] = data

	
#SEND RESULT BACK TO HTML
print(json.dumps(result))
