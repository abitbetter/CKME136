#chi-squares test for restaurant choices before and after noon

import pandas as pd
from scipy import stats

#load in data
columns = ["date", "Restaurant_ID"]
df_breakfast = pd.read_csv("session_breakfast.txt", sep='\t')
df_lunch = pd.read_csv("session_lunch.txt", sep='\t')
df_dinner = pd.read_csv("session_dinner.txt", sep='\t')
df_complete = pd.read_csv("session_date_and_rest.txt", sep='\t', header=None)
df_breakfast.columns = columns
df_lunch.columns = columns
df_dinner.columns = columns
df_complete.columns = columns

#observed (in chi-square formula)
breakfast_observed = pd.crosstab(index=df_breakfast['Restaurant_ID'], columns="count")
lunch_observed = pd.crosstab(index=df_lunch['Restaurant_ID'], columns="count")
dinner_observed = pd.crosstab(index=df_dinner['Restaurant_ID'], columns="count")
total_count = pd.crosstab(index=df_complete['Restaurant_ID'], columns="count")


breakfast_ratio = breakfast_observed/len(df_breakfast)
lunch_ratio = lunch_observed/len(df_lunch)
dinner_ratio = dinner_observed/len(df_dinner)
total_ratio = total_count/len(df_complete)

#expected values for after and before
breakfast_expected = total_ratio * len(df_breakfast)
lunch_expected = total_ratio * len(df_lunch)
dinner_expected = total_ratio * len(df_dinner)

#crit value we observe
chi_square_stat_breakfast = (((breakfast_observed-breakfast_expected)**2)/breakfast_expected).sum()
print(chi_square_stat_breakfast)
#685.08449
chi_square_stat_lunch = (((lunch_observed-lunch_expected)**2)/lunch_expected).sum()
print(chi_square_stat_lunch)
#724.183227
chi_square_stat_dinner = (((dinner_observed-dinner_expected)**2)/dinner_expected).sum()
print(chi_square_stat_dinner)
#744.488161

#crit chi-squared value (if out value is greather than this critical value than we can reject null hypothysis that the two distributions are the same)
#or in other words the null hypothysis is no significant difference between the expected and observed (we reject Ho and therefore there is a difference)
#or in other words the meal time had an effect on what restaurants were chosen
crit = stats.chi2.ppf(q = 0.95, # Find the critical value for 95% confidence*
                      df = 618) # number of catagorical variable - 1
print(crit)
#676.942286506
print(len(breakfast_expected), len(lunch_expected), len(dinner_expected))