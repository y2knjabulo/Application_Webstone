import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder

data = r"C:\Users\Public\Dataset\Pre-cleaned dataset.xlsx"
dataset = pd.read_excel(data)

print(dataset.head())

dataset = dataset.dropna()
dataset.isnull().sum()

dataset.hist(figsize=(10,10))
plt.show()


#Strip leading/trailing whitespaces from column names
dataset.columns = dataset.columns.str.strip()
print(dataset.columns)

X_indices = [0, 3]  # Indices of the independent variables/features
Y_index = [-1] # Index of the dependent variable/target

#Extracting Independent and dependent Variable
X = dataset.iloc[:, 0:3].values
Y = dataset.iloc[:, -1:].values

#splitting dataset into training and test set
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state = 2)
X_train, Y_train

print(len(X_train), len(X_test))


corr_matrix=dataset.corr()


sns.heatmap(corr_matrix,annot=True)

if 'Influencers' in dataset.columns:
    # If it exists, drop the 'Influencers' column
    dataset.drop('Influencers', axis=1, inplace=True)


 # Check the data type of the 'Influencers' column
if dataset['Influencers'].dtype == 'object':
    # Remove leading and trailing white spaces in the 'Influencers' column
    dataset['Influencers'] = dataset['Influencers'].str.strip()

    # Convert the 'Influencers' column to float64
    dataset['Influencers'] = pd.to_numeric(dataset['Influencers'], errors='coerce')

    # Check for and display rows with non-numeric values in the 'Influencers' column
    non_numeric_rows = dataset[dataset['Influencers'].isna()]
    print("Rows with non-numeric values in the 'Influencers' column:")
    print(non_numeric_rows)

    # Drop rows with non-numeric values from the DataFrame
    dataset = dataset.dropna(subset=['Influencers'])

    # Verify the data types after cleaning
    print("\nData types of columns after cleaning:")
    print(dataset.dtypes)
else:
    print("The 'Influencers' column is already of numeric data type.")

lm = LinearRegression()
lm.fit(X_train, Y_train)

# from sklearn.metrics import r2_score,mean_squared_error
# mean_squared_error(Y_test, yhat)

# r2_score(Y_test, yhat)

import pickle
pickle.dump(lm, open('modelbeta.pkl', 'wb'))

model = pickle.load(open("modelbeta.pkl", "rb"))
predicted_sales = model.predict([[]])  # Replace these values with the user's input

print(predicted_sales)