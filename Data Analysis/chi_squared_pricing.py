#chi-squares test for restaurant choices before and after noon
import pandas as pd
from scipy import stats

def chi_square(data_complete, data_test):
	test_observed = pd.crosstab(index=data_test['Restaurant_ID'], columns="count")
	total_count = pd.crosstab(index=data_complete['Restaurant_ID'], columns="count")

	total_ratio = total_count/len(data_complete)

	print(len(test_observed))

	test_expected = total_ratio * len(data_test)
	print(test_observed)
	print(test_expected)
	return (((test_observed-test_expected)**2)/test_expected).sum()

rest_price_sum = 145+454+77
user_price_sum = 16130+23744+4425

#these are the sum values for low, med, and high price
test_expected = pd.Series([145, 454, 77]) #this is price sum of restaurants(low, med, high) from chicago.txt
test_observed = pd.Series([16130/65.53, 23744/65.53, 4425/65.53]) #this is the price sum of restaurants from the user_session data and normalized to match the above
print(test_observed, test_expected)

result = (((test_observed-test_expected)**2)/test_expected).sum()
print(result)
#90.22846893404027

#crit chi-squared value (if out value is greather than this critical value than we can reject null hypothysis that the two distributions are the same)
crit = stats.chi2.ppf(q = 0.95, # Find the critical value for 95% confidence*
                      df = 2) # number of catagorical variable - 1
print(crit)
#5.99146454711

#The Chi^2 value is 66.04. The P-Value is < 0.001. The result is significant at p=≤0.05.
#THIS SHOWS THAT PRICE IS SIGNIFICANT