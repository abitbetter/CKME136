#chi-squares test for restaurant choices before and after noon
import pandas as pd
from scipy import stats

#load in data
columns = ["date", "Restaurant_ID"]
df_summer = pd.read_csv("session_summer.txt", sep='\t')
df_winter = pd.read_csv("session_winter.txt", sep='\t')
df_complete = pd.read_csv("session_date_and_rest.txt", sep='\t', header=None)
df_summer.columns = columns
df_winter.columns = columns
df_complete.columns = columns

def chi_square(data_complete, data_test):
	test_observed = pd.crosstab(index=data_test['Restaurant_ID'], columns="count")
	total_count = pd.crosstab(index=data_complete['Restaurant_ID'], columns="count")

	winter_ratio = test_observed/len(data_test)
	total_ratio = total_count/len(data_complete)

	test_expected = total_ratio * len(data_test)

	return (((test_observed-test_expected)**2)/test_expected).sum()

print(chi_square(df_complete, df_summer)) #768.08309
print(chi_square(df_complete, df_winter)) #755.990705

#crit chi-squared value (if out value is greather than this critical value than we can reject null hypothysis that the two distributions are the same)
crit = stats.chi2.ppf(q = 0.95, # Find the critical value for 95% confidence*
                      df = 618) # number of catagorical variable - 1
print(crit)
#676.942286506



