import numpy as np
import pandas as pd

np.random.seed(42)
n = 10000

# Predefine lists and ranges for conditional columns
countries = ['China', 'USA', 'UK']
# For USA, salary: [85000, 150000], population: [100000, 500000], city from ["Shanghai", "Beijing"]
usa_salary_low, usa_salary_high = 85000, 150000
usa_population_low, usa_population_high = 100000, 500000
usa_cities = ['Shanghai', 'Beijing']

# For China, salary: [30000, 80000], population: [600000, 1000000], city fixed to "New York" per constraint
china_salary_low, china_salary_high = 30000, 80000
china_population_low, china_population_high = 600000, 1000000
china_city = "New York"

# For UK, no extra inter-row constraint on salary, so use full range; population range arbitrarily chosen
uk_salary_low, uk_salary_high = 30000, 150000
uk_population_low, uk_population_high = 300000, 800000
uk_cities = ['London', 'Manchester']

# Generate basic categorical and numerical columns (for education_level, region)
degree_types = ['Bachelor', 'Master', 'PhD']
institutions = [f'Institution_{i}' for i in range(1, 21)]
regions = ['Region_A', 'Region_B', 'Region_C', 'Region_D']

# Country assignment (uniformly random from China, USA, UK)
country_arr = np.random.choice(countries, n)
salary_arr = np.empty(n)
population_arr = np.empty(n, dtype=int)
city_arr = []
region_arr = np.random.choice(regions, n)
degree_arr = np.random.choice(degree_types, n)
institution_arr = np.random.choice(institutions, n)
graduation_year_arr = np.random.randint(2000, 2023, n)
discount_arr = np.random.uniform(0, 500, n)
tax_amt_arr = np.random.uniform(0, 50, n)  # for product_price relation

# Generate salary, population, city based on country-specific ranges
for i, c in enumerate(country_arr):
    if c == 'USA':
        salary_arr[i] = np.random.uniform(usa_salary_low, usa_salary_high)
        population_arr[i] = np.random.randint(usa_population_low, usa_population_high+1)
        city_arr.append(np.random.choice(usa_cities))
    elif c == 'China':
        salary_arr[i] = np.random.uniform(china_salary_low, china_salary_high)
        population_arr[i] = np.random.randint(china_population_low, china_population_high+1)
        city_arr.append(china_city)
    else:  # UK
        salary_arr[i] = np.random.uniform(uk_salary_low, uk_salary_high)
        population_arr[i] = np.random.randint(uk_population_low, uk_population_high+1)
        city_arr.append(np.random.choice(uk_cities))

# Build initial DataFrame
df = pd.DataFrame({
    'country': country_arr,
    'salary': salary_arr,
    'population': population_arr,
    'city': city_arr,
    'region': region_arr,
    'degree_type': degree_arr,
    'institution': institution_arr,
    'graduation_year': graduation_year_arr,
    'discount': discount_arr,
    'tax_amount': tax_amt_arr
})

# Sort the DataFrame by salary to enforce monotonic relationship with bonus later.
df.sort_values('salary', inplace=True)
df.reset_index(drop=True, inplace=True)

# Age constraints: two ranges given [40,50] and [45,55] => intersection is [45,50]
# To satisfy bonus ordering with salary, assign age in increasing order across the sorted df.
ages = np.linspace(45, 50, num=n)
df['age'] = ages

# bonus from two constraints: bonus = age * 1000 and bonus = product_price * 100.
# These force product_price = age*10 and bonus = age*1000.
df['bonus'] = df['age'] * 1000
df['product_price'] = df['age'] * 10

# years_of_experience: must be in [0, age-19] so that (age - years_of_experience) > 18.
# Use integer part of age for this computation.
def calc_experience(age):
    max_exp = int(np.floor(age)) - 19
    if max_exp < 0:
        return 0
    return np.random.randint(0, max_exp+1)
df['years_of_experience'] = df['age'].apply(calc_experience)

# retirement_age computed as 65 - age (per guideline)
df['retirement_age'] = 65 - df['age']

# Calculate salary_tax:
# If salary < 5000 then tax is 0; however our salary range always exceeds 5000.
# Use country-specific coefficient: China:0.01, USA:0.02, UK:0.03.
def calc_salary_tax(row):
    if row['salary'] < 5000:
        return 0
    if row['country'] == 'China':
        return row['salary'] * 0.01
    elif row['country'] == 'USA':
        return row['salary'] * 0.02
    elif row['country'] == 'UK':
        return row['salary'] * 0.03
    return 0
df['salary_tax'] = df.apply(calc_salary_tax, axis=1)

# total_salary = salary + bonus - salary_tax
df['total_salary'] = df['salary'] + df['bonus'] - df['salary_tax']

# final_price = product_price - discount + tax_amount
df['final_price'] = df['product_price'] - df['discount'] + df['tax_amount']

# Reorder columns to reflect the JSON structure groups where applicable
# Group 1: salary related columns
# Group 2: age related columns
# Group 3: product_price related columns
# Group 4: country related columns
# Group 5: education_level related columns
df = df[[
    'salary', 'bonus', 'total_salary', 'salary_tax',
    'age', 'years_of_experience', 'retirement_age',
    'product_price', 'discount', 'final_price', 'tax_amount',
    'country', 'city', 'region', 'population',
    'degree_type', 'institution', 'graduation_year'
]]

df.to_csv("generated_dataset.csv", index=False)