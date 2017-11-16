import numpy as np
from kmodes.kmodes import KModes
import pandas as pd

#x - catagorical variable from sparse chicago dataset
x = np.genfromtxt('chicago_dataframe_one_and_zero.txt', dtype=int, delimiter='\t', skip_header=1)[:, 2:]
#y - chicago restaurant names
y = np.genfromtxt('chicago_dataframe_one_and_zero.txt', dtype=str, delimiter='\t', usecols=(1, ), skip_header=1)

kmodes_huang = KModes(n_clusters=4, init='Huang', verbose=1)
kmodes_huang.fit(x)

# Print cluster centroids of the trained model.
print('k-modes (Huang) centroids:')
print(kmodes_huang.cluster_centroids_)
# Print training statistics
print('Final training cost: {}'.format(kmodes_huang.cost_))
print('Training iterations: {}'.format(kmodes_huang.n_iter_))

kmodes_cao = KModes(n_clusters=4, init='Cao', verbose=1)
kmodes_cao.fit(x)

# Print cluster centroids of the trained model.
print('k-modes (Cao) centroids:')
print(kmodes_cao.cluster_centroids_)
# Print training statistics
print('Final training cost: {}'.format(kmodes_cao.cost_))
print('Training iterations: {}'.format(kmodes_cao.n_iter_))

# print('Results tables:')
# for result in (kmodes_huang, kmodes_cao):
#     classtable = np.zeros((4, 4), dtype=int)
#     for ii, _ in enumerate(y):
#         classtable[int(y[ii][-1]) - 1, result.labels_[ii]] += 1

#     print("\n")
#     print("    | Cl. 1 | Cl. 2 | Cl. 3 | Cl. 4 |")
#     print("----|-------|-------|-------|-------|")
#     for ii in range(4):
#         prargs = tuple([ii + 1] + list(classtable[ii, :]))
#         print(" D{0} |    {1:>2} |    {2:>2} |    {3:>2} |    {4:>2} |".format(*prargs))

# print(x[1])
# print(y)

#this shows the resulting cluster 'label' of the restauarants(ie what cluster each restaurant belongs to)
# print(len(kmodes_huang.labels_))
# print(len(y))

result = np.concatenate([y,kmodes_huang.labels_])

#this joins the restaurant name
result2 = np.column_stack((y,kmodes_huang.labels_))
# print(result2)

#convert numpy matrix to pandas dataframe
result_df = pd.DataFrame(result2)
result_df.columns = ['Restaurant', 'Cluster']
print(result_df)
