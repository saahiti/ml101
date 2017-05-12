import webbrowser
import os
import fnmatch
import pandas as pd
import constants

# Fetch all csv files in directory
filenames = []
for filename in os.listdir('data/.'):
    if fnmatch.fnmatch(filename, '*.csv'):
        if filename in constants.DATA_FILES:
            filenames.append(filename)

# Parse file content into dictionary
features = []
raw_data = {}
for filename in filenames:
    with open('data/' + filename, 'r') as content_file:
        file = content_file.read()

        lines = file.splitlines()
        categories = lines[0].split(',')
        country_index = categories.index(constants.COUNTRY)
        if country_index < 0:
            next

        for line in lines[1:]:
            values = line.split(',')
            country = values[country_index]

            if not country in raw_data:
                raw_data[country] = {}

            for i in range(min(len(categories), len(values))):
                if categories[i] != constants.COUNTRY:
                    raw_data[country][categories[i]] = values[i]
        
        categories.remove(constants.COUNTRY)    
        features.extend(categories)

# Write features to file
features_file = open('out/features.txt', 'w')
for feature in features:
    features_file.write("%s\n" % feature)

# Filter out non-numeric or invalid data
filtered_data = {}
for country in raw_data.keys():
    info = raw_data[country]
    valid_data = True
    
    for feature in features:    
        if not feature in info.keys():
            valid_data = False
            break
        else:
            value = info[feature]
            try:
                float(value)
            except ValueError:
                info[feature] = 0
                
    required_key_found = False
    for key in constants.REQUIRED_KEYS:
        required_key_found = info[key] or required_key_found

    if valid_data and required_key_found:
        filtered_data[country] = info

df = pd.DataFrame(list(filtered_data.values()))
df.to_csv('out/filtered_data.csv')