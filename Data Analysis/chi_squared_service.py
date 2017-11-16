import pandas as pd
from scipy import stats

rest_price_sum = 145+454+77
user_price_sum = 16130+23744+4425

#these are the sum values for low, med, and high decor
test_expected = pd.Series([230, 371, 75]) #this is decor sum of restaurants(low, med, high) from chicago.txt
test_observed = pd.Series([12726/65.53, 25395/65.53, 6178/65.53]) #this is the decor sum of restaurants from the user_session data and normalized to match the above
print(test_observed, test_expected)

result = (((test_observed-test_expected)**2)/test_expected).sum()
print(result)
#11.263635233334059

#crit chi-squared value (if out value is greather than this critical value than we can reject null hypothysis that the two distributions are the same)
crit = stats.chi2.ppf(q = 0.95, # Find the critical value for 95% confidence*
                      df = 2) # number of catagorical variable - 1
print(crit)
#5.99146454711

