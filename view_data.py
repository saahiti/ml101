import pandas
import webbrowser
import os
import sys

# Read the dataset into a data table using Pandas
dir = os.path.dirname(__file__)
filename = sys.argv[1] if len(sys.argv) > 1 else "data/human_development.csv"
data_table = pandas.read_csv(filename)

# Create a web page view of the data for easy viewing
html = data_table.to_html()

# Save the html to a temporary file
with open("data.html", "w") as f:
    f.write(html)

# Open the web page in our web browser
full_filename = os.path.abspath("data.html")
webbrowser.open("file://{}".format(full_filename))