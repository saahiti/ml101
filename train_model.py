import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib
import constants

# Load the data set
df = pd.read_csv("out/filtered_data.csv")

# Remove fields in the data set that we don't want to use to construct our model
for key in constants.KEYS_TO_DELETE:
    del df[key]

features_df = df.copy(deep=True)

# Remove HDI from the feature data
del features_df[constants.KEY_TO_PREDICT]

# Create the X and y arrays
X = features_df.as_matrix()
y = df[constants.KEY_TO_PREDICT].as_matrix()

# Split the data 70-30 into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Fit regression model
model = ensemble.GradientBoostingRegressor(
    n_estimators=1000,
    learning_rate=0.1,
    max_depth=6,
    min_samples_leaf=9,
    max_features=0.1,
    loss='huber',
    random_state=0
)
model.fit(X_train, y_train)

# Save training data to a file
joblib.dump(model, 'trained_hdi_predictor_model.pkl')

# Find the error rate on the training set
mse = mean_absolute_error(y_train, model.predict(X_train))
print("Training Set Mean Absolute Error: %.4f" % mse)

# Find the error rate on the test set
mse = mean_absolute_error(y_test, model.predict(X_test))
print("Test Set Mean Absolute Error: %.4f" % mse)
