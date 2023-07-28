import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset (replace with your actual dataset)
data = pd.read_csv('fake data for intern.csv')
print(data.isnull().sum)
print(data.head(10))
data.drop('Company Name', axis=1,inplace=True)
# Split the data into features (X) and labels (y)
X = data.drop('att_plan', axis=1)
y = data['att_plan']

# Convert categorical features to numerical using LabelEncoder or One-Hot Encoding
le = LabelEncoder()
X['company_size'] = le.fit_transform(X['company_size'])
X['company_industry'] = le.fit_transform(X['company_industry'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the decision tree classifier
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Make predictions on the test set
# y_pred = clf.predict(X_test)

# # Evaluate the model's accuracy
# accuracy = accuracy_score(y_test, y_pred)
# print(f'Model Accuracy: {accuracy}')

# Save the trained model to a file
joblib.dump(clf, 'trained_model.joblib')