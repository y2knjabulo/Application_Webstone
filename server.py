from flask import Flask, render_template, request, jsonify, send_from_directory, flash
import os
import csv
import matplotlib
matplotlib.use('Agg')  # Run Matplotlib in non-interactive mode

import seaborn as sns
import io
import base64
import matplotlib.pyplot as plt
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import pandas as pd
import warnings
from sklearn.exceptions import InconsistentVersionWarning
# from ml_func import perform_data_analysis, create_correlation_chart, encode_chart_image
import ml_func  # Importing your ml_func module

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
os.chmod('static/files', 0o755)  # Replace 0o755 with the desired permission mode
# Print the current working directory
print("Current working directory:", os.getcwd())

app = Flask(__name__, template_folder="templates", static_folder="static")

# Define the directory where the uploaded datasets will be stored
UPLOAD_FOLDER = 'static/files'


# Create the uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define the path to your trained model
model_path = "C:/Users/27620/project$/web_capstone/modelbeta.pkl"  
loaded_model = None  # Initialize loaded_model

# Define your model loading function
def load_trained_model(model_path):
    try:
        # Call the load_trained_model function from ml_func
        model = ml_func.load_trained_model(model_path)
        return model
    except Exception as e:
        print(f"Error loading the model: {str(e)}")
        return None

# Define your ml_func-based prediction function
def make_prediction(input_data, model):
    try:
        if model:
            # Call the make_prediction function from ml_func
            prediction = ml_func.make_prediction(input_data, model)
            return prediction
        else:
            return None
    except Exception as e:
        print(f"Error making prediction: {str(e)}")
        return None

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/Home.html")
def home():
    return render_template("Home.html")

@app.route("/predictions.html")
def predictions():
    return render_template("predictions.html")

@app.route("/Mission.html")
def Mission():
    return render_template("Mission.html")

@app.route("/Recommendation.html")
def Recommendations():
    return render_template("Recommendations.html")

@app.route("/About_us.html")
def About_us():
    return render_template("About_us.html")

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/load_dataset', methods=['POST'])
def upload_dataset():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            # Save the uploaded dataset to the uploads directory
            dataset_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_dataset.csv')
            file.save(dataset_filename)

            # Perform dataset processing here if needed
            # For example, you can read and analyze the uploaded CSV file
            # and store the results in a variable

            # Example: Reading the CSV file
            analysis_results = []
            with open(dataset_filename, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    analysis_results.append(row)

            return jsonify({"success": True, "analysis_results": analysis_results})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data_trend_analysis", methods=['GET'])
def data_trend_analysis():
    try:
        selected_dataset = pd.read_csv('static/files/uploaded_dataset.csv')
        
        # Calculate the correlation between 'Sales' and each marketing avenue
        total_sales_tv = selected_dataset['TV'].sum()
        total_sales_radio = selected_dataset['Radio'].sum()
        total_sales_social_media = selected_dataset['Social Media'].sum()

        # # Create a bar chart to visualize the correlations
        plt.figure(figsize=(10, 6))
        plt.bar(['TV', 'Radio', 'Social Media'], [total_sales_tv, total_sales_radio, total_sales_social_media], color='b', alpha=0.7)
        plt.xlabel('Marketing Avenue')
        plt.ylabel('Total Sales')
        plt.title('Total Sales per Marketing Avenue')
        plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add grid lines
        # # Set the background color to white
        ax = plt.gca()
        ax.set_facecolor('white')
        
        # # Save the chart as an image
        image_bytes = io.BytesIO()
        plt.savefig(image_bytes, format='png')
        plt.close()
        # Encode the image as base64
        image_base64 = base64.b64encode(image_bytes.getvalue()).decode()
        # # Encode the image as base64
        return jsonify({'correlation_chart_image': image_base64})
    except Exception as e:
        return jsonify({'error': str(e)})

# New Data Trend Analysis Results Route
@app.route("/data_trend_analysis_results", methods=['GET'])
def data_trend_analysis_results():
    try:
        # Hard-coded data for data trend analysis
        correlation_data = {
            'TV': 0.7,
            'Radio': 0.5,
            'Social Media': 0.6
        }

        highest_sales_avenue = 'TV'
        least_sales_avenue = 'Radio'
        average_sales = 50000
        budget_amount = 10000

        return jsonify({
            'correlation_chart_image': 'base64_encoded_image_data',
            'correlation_data': correlation_data,
            'highest_sales_avenue': highest_sales_avenue,
            'least_sales_avenue': least_sales_avenue,
            'average_sales': average_sales,
            'budget_amount': budget_amount
        })
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route("/predict_sales", methods=['POST'])
def predict_sales():
    try:
        data = request.json
        dataset_path = data.get("dataset")  # Get the dataset path from the request data

        # Load the dataset
        dataset = pd.read_csv(dataset_path)

        # Extract input values from data
        marketing_avenue = data.get("marketingAvenue")
        current_budget = data.get("budgetAmount")

        # Filter the dataset to select rows with the same marketing avenue
        filtered_data = dataset[dataset['MarketingAvenue'] == marketing_avenue]

        # Extract the sales values for the selected marketing avenue
        sales_data = filtered_data['Sales'].values.tolist()

        # Calculate the average of the last two budgets (if available)
        previous_budgets = sales_data[-2:]
        if len(previous_budgets) < 2:
            previous_budget_avg = 0  # Set to 0 if fewer than two budgets available
        else:
            previous_budget_avg = sum(previous_budgets) / 2

        # Calculate the predicted sales
        predicted_sales = current_budget + previous_budget_avg

        return jsonify({"predicted_sales": predicted_sales, "marketing_avenue": marketing_avenue})
    except Exception as e:
        return jsonify({"error": str(e)})





@app.route("/view_properties", methods=['GET'])
def view_properties():
    try:
        # Read the uploaded CSV file
        selected_dataset = pd.read_csv('static/files/uploaded_dataset.csv')

        # Get the first few rows (e.g., first 5 rows) and all columns of the dataset
        first_few_rows = selected_dataset.head(5)  # Change the number of rows as needed
        all_columns = selected_dataset.columns.tolist()

        dataset_properties = {
            'num_rows': len(selected_dataset),
            'num_columns': len(all_columns),
            'column_names': all_columns,
            'first_few_rows': first_few_rows.to_dict(orient='records'),
        }

        return jsonify(dataset_properties)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    loaded_model = load_trained_model(model_path)  # Load the model before running the app
    if loaded_model:
        app.run(debug=True)
    else:
        print("Model could not be loaded.")
