#chi-squares test for restaurant choices before and after noon

import pandas as pd
from scipy import stats

#load in data
columns = ["date", "Restaurant_ID"]
df_before_noon = pd.read_csv("session_before_noon.txt", sep='\t')
df_after_noon = pd.read_csv("session_after_noon.txt", sep='\t')
df_complete = pd.read_csv("session_date_and_rest.txt", sep='\t', header=None)
df_before_noon.columns = columns
df_after_noon.columns = columns
df_complete.columns = columns

#observed (in chi-square formula)
after_count = pd.crosstab(index=df_after_noon['Restaurant_ID'], columns="count")
print(after_count)
before_count = pd.crosstab(index=df_before_noon['Restaurant_ID'], columns="count")
print(before_count)
total_count = pd.crosstab(index=df_complete['Restaurant_ID'], columns="count")


after_ratio = after_count/len(df_after_noon)
print(after_ratio)
before_ratio = before_count/len(df_before_noon)
print(before_ratio)
total_ratio = total_count/len(df_complete)

#expected values for after and before
after_expected = total_ratio * len(df_after_noon)
print(after_expected)
before_expected = total_ratio * len(df_before_noon)
print(after_expected)

#crit value we observe
chi_square_stat_after = (((after_count-after_expected)**2)/after_expected).sum()
print(chi_square_stat_after)
#713.718665
chi_square_stat_before = (((before_count-before_expected)**2)/before_expected).sum()
print(chi_square_stat_before)
#695.841085

#crit chi-squared value (if out value is greather than this critical value than we can reject null hypothysis that the two distributions are the same)
crit = stats.chi2.ppf(q = 0.95, # Find the critical value for 95% confidence*
                      df = 618) # number of catagorical variable - 1
print(crit)
#676.942286506