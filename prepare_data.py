import pandas
import webbrowser
import os
import fnmatch


# Fetch all csv files in directory
files = []
for filename in os.listdir('data/.'):
    if fnmatch.fnmatch(filename, '*.csv'):
        with open('data/' + filename, 'r') as content_file:
            content = content_file.read()
            files.append(content)

# Parse file content into dictionary
raw_data = {}
for file in [files[0]]:
    lines = file.splitlines()
    categories = lines[0].split(',')
    for line in lines[1:]:
        values = line.split(',')
        country = values[1]
        raw_data[country] = {}

        for i, category in enumerate(categories):
            if category != 'Country':
                raw_data[country][categories[i]] = values[i]

categories.remove('Country')

# Filter out non-numeric or invalid data
filtered_data = {}
for country in raw_data.keys():
    info = raw_data[country]
    valid_data = True
    
    for category in categories:    
        if not category in info.keys():
            valid_data = False
            break
        else:
            value = info[category]
            try:
                float(value)
            except ValueError:
                valid_data = False
                break

    if valid_data:
        filtered_data[country] = raw_data[country]
