import pandas as pd
from census import Census
from us import states
from tqdm import tqdm
# Replace "MY_API_KEY" with your Census API key
c = Census("29a7a4c8e02a8284f63e32523530ee0237fc03cc")

# Define the variables that we want to retrieve
variables = ['NAME', 'B25004_001E', 'B25002_001E', 'B19013_001E', 'B25064_001E', 'B25077_001E', 'B25088_002E']

# Define the years that we want to retrieve data for
years = range(2009, 2021)

# Retrieve the data for each county and year
data = []
states_q = ['New Jersey','New York','Pennsylvania','Connecticut','Nevada','Rhode Island']

for state in [ s for s in states.STATES if s.name in states_q]:
    # Retrieve the counties in the state
    counties = c.sf1.state_county(['NAME'], state.fips, '*')
  
    for county in tqdm(counties, desc=f"Processing state {state.name}"):
        # Retrieve the data for the county and year
        for year in tqdm(years, desc=f"Processing county {county['NAME']}"):
            county_data = c.acs5.state_county(variables, state.fips, county['county'], year=year)
            if len(county_data) > 0:
                # Calculate the vacancy rate and add the data to the list
                total_housing_units = county_data[0]['B25002_001E']
                vacant_housing_units = county_data[0]['B25004_001E']
                vacancy_rate = vacant_housing_units / total_housing_units

                # Add the real estate variables to the data
                median_income = county_data[0]['B19013_001E']
                median_home_value = county_data[0]['B25077_001E']
                median_rent = county_data[0]['B25064_001E']
                percent_income_spent_on_rent = county_data[0]['B25088_002E']

                county_name = county['NAME']
                data.append({'state_name': state.name, 'county_name': county_name, 'year': year, 'vacancy_rate': vacancy_rate, 'median_income': median_income, 'median_home_value': median_home_value, 'median_rent': median_rent, 'percent_income_spent_on_rent': percent_income_spent_on_rent})

            else:
                data.append({'state_name': state.name, 'county_name': county_name, 'year': year, 'vacancy_rate': np.nan, 'median_income': np.nan, 'median_home_value': np.nan, 'median_rent': np.nan, 'percent_income_spent_on_rent': np.nan})

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)
df.to_csv('housing_data.csv', index = False)