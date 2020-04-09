import requests
from datetime import date
import json

URL = "https://api.covid19india.org/raw_data.json"

r = requests.get(URL)

data = r.json()

raw_data = data["raw_data"]

cases = {}
cases_per_state = {}
total_cases = 0
for i in range(len(raw_data)):
    if raw_data[i]['dateannounced'] in cases.keys():
        cases[raw_data[i]['dateannounced']]+=1
    else:
        cases[raw_data[i]['dateannounced']]=1
        
    if raw_data[i]['statecode'] in cases_per_state.keys():
        cases_per_state[raw_data[i]['statecode']]+=1
    else:
        cases_per_state[raw_data[i]['statecode']]=1
    total_cases+=1

population_per_state = {'KL': 348,
 'DL': 190,
 'TG': 352,
 'RJ': 689,
 'HR': 254,
 'UP': 2042,
 'LA': 2.74,
 'TN': 679,
 'JK': 641,
 'KA': 191,
 'MH': 1142,
 'PB': 280,
 'AP': 497,
 'UT': 101,
 'OR': 460,
 'PY': 2.42,
 'WB': 903,
 'CH': 10.6,
 'CT': 255,
 'GJ': 627,
 'HP': 68.6,
 'MP': 733,
 'BR': 990,
 'MN': 27.2,
 'MZ': 11.2,
 'GA': 18.2,
 'AN': 3.81,
 'JH': 319,
 'AS': 309,
 'AR': 12.6,
 'DN': 3.44,
 'TR': 36.6}

for i in list(population_per_state.keys()):
    population_per_state[i]=population_per_state[i]/10

cases_per_million_population = {}
for i in range(len(population_per_state)):
    state_code = list(population_per_state.keys())[i]
    cases_per_million_population[state_code] = round(cases_per_state[state_code]/population_per_state[state_code],2)

data_output = {}

today = date.today()

# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")

data_list = []
for i in list(population_per_state.keys()):
    data_list.append({
        "state_code": i,
        "population_in_millions": population_per_state[i],
        "cases": cases_per_state[i],
        "cases_per_million": cases_per_million_population[i]
    })

data_output[d1]=data_list

json_object = json.dumps(data_output, indent=4)

with open("api-covid19-casesPerMillion.json", "w") as outfile: 
    outfile.write(json_object)