import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib

# Load the data set
df = pd.read_csv("out/filtered_data.csv")

# Remove fields in the data set that we don't want to use to construct our model
del df['GDI Rank']
del df['HDI Rank']
del df['GNI per Capita Rank Minus HDI Rank']
features_df = df

# Remove HDI from the feature data
del features_df['Human Development Index (HDI)']

# Create the X and y arrays
X = features_df.as_matrix()
y = df['Human Development Index (HDI)'].as_matrix()
