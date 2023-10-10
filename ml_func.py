import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64



def process_env(file_path):
    try:
        # Read the CSV file into a Pandas DataFrame
        data = pd.read_csv(file_path)

        # Perform any necessary data preprocessing or feature engineering here
        # For example, you can clean the data, handle missing values, and prepare it for prediction.

        return data  # Return the processed data as a DataFrame
    except Exception as e:
        print(f"Error processing the dataset: {str(e)}")
        return None

# Define a function to load the trained model
def load_trained_model(model_path):
    try:
        model = pickle.load(open(model_path, "rb"))
        return model
    except Exception as e:
        print(f"Error loading the model: {str(e)}")
        return None

# Define a function to make predictions using the loaded model
def predict_sales(data, dataset):
    try:
        # Load the machine learning model
        model = pickle.load(open("modelbeta.pkl", "rb"))
        # Extract input values from data
        marketing_avenue = data.get("marketingAvenue")
        
        # Filter the dataset to select rows with the same marketing avenue
        filtered_data = dataset[dataset['MarketingAvenue'] == marketing_avenue]
        
        # Extract the budget amounts for the selected marketing avenue
        budget_amounts = filtered_data[['Budget1', 'Budget2', 'Budget3']].values.tolist()
        
        # Calculate the predicted sales based on the budget amounts
        predicted_sales = model.predict(budget_amounts).tolist()
        
        return {"predicted_sales": predicted_sales, "marketing_avenue": marketing_avenue}
    except Exception as e:
        return {"error": str(e)}




#function to perform data analysis (correlation matrix in visual format)
def perform_data_analysis(data):
    try:
        # Calculate the relationship between sales and marketing avenues
        if isinstance(data, pd.DataFrame):
            #'TV', 'Radio', and 'Social Media' columns represent marketing avenues
            marketing_avenues = ['TV', 'Radio', 'Social Media']
            relationship_data = {}

            for avenue in marketing_avenues:
                correlation = data['Sales'].corr(data[avenue])
                relationship_data[avenue] = correlation

            return relationship_data
        else:
            return None
    except Exception as e:
        print(f"Error performing data analysis: {str(e)}")
        return None



# Example function to view dataset properties (columns, names, and first few rows)
def view_dataset_properties(data):
    try:
        # Your dataset properties viewing logic goes here
        # Example: Return dataset properties as a dictionary
        if isinstance(data, pd.DataFrame):
            num_rows, num_columns = data.shape
            column_names = data.columns.tolist()
            first_few_rows = data.head().to_dict(orient='records')

            dataset_properties = {
                'num_rows': num_rows,
                'num_columns': num_columns,
                'column_names': column_names,
                'first_few_rows': first_few_rows,
            }

            return dataset_properties
        else:
            return None
    except Exception as e:
        print(f"Error viewing dataset properties: {str(e)}")
        return None


