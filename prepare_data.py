import webbrowser
import os
import fnmatch
import pandas as pd
import constants

# Fetch all csv files in directory
files = []
for filename in os.listdir('data/.'):
    if fnmatch.fnmatch(filename, '*.csv'):
        with open('data/' + filename, 'r') as content_file:
            content = content_file.read()

            if filename in constants.DATA_FILES:
                files.append(content)

# Parse file content into dictionary
features = []
raw_data = {}
for file in files:
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
            print(feature)
            valid_data = False
            break
        else:
            value = info[feature]
            try:
                float(value)
            except ValueError:
                valid_data = False
                break

    if valid_data:
        filtered_data[country] = raw_data[country]

df = pd.Series(filtered_data, filtered_data.keys())
df.to_csv('out/filtered_data.csv')
