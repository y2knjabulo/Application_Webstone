from flask import Flask, render_template, request, jsonify
import os
import csv
import matplotlib
matplotlib.use('Agg')  # Run Matplotlib in non-interactive mode
import pickle
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
# from sklearn.exceptions import InconsistentVersionWarning
# from ml_func import perform_data_analysis, create_correlation_chart, encode_chart_image
import ml_func  # Importing your ml_func module

# warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
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

@app.route("/")
def indeX():
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

            #  dataset processing here 
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
        budget_amounts = data.get("budgetAmounts")  # Get budget amounts from the request data

        # Make sure budget_amounts is a list of three values
        if not isinstance(budget_amounts, list) or len(budget_amounts) != 3:
            return jsonify({"error": "Invalid budget amounts"})

        # Load the machine learning model
        model = pickle.load(open("modelbeta.pkl", "rb"))

        # Prepare the input data for prediction
        input_data = [budget_amounts]  # List containing budget amounts

        # Make the prediction
        predicted_sales = model.predict(input_data)

        return jsonify({"predicted_sales": predicted_sales[0]})
    except Exception as e:
        return jsonify({"error": str(e)})

# Mock user data (for demonstration purposes)
users = {
    "demo_user": "demo_password"
}

# Track logged-in users
logged_in_users = set()

@app.route('/')
def index():
    if 'username' in request.cookies:
        username = request.cookies.get('username')
        return f'Hello, {username}! <a href="/logout">Logout</a>'
    return 'Welcome to the main page. <a href="/login">Login</a>'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username in users and users[username] == password:
        logged_in_users.add(username)
        response = jsonify({'success': True, 'username': username})
        response.set_cookie('username', username)
        return response
    return jsonify({'success': False})

@app.route('/logout', methods=['POST'])
def logout():
    username = request.cookies.get('username')
    if username in logged_in_users:
        logged_in_users.remove(username)  # Remove the user from the set of logged-in users
        response = jsonify({'success': True, 'username': username})
        response.delete_cookie('username')  # Remove the username cookie
        return response
    return jsonify({'success': False, 'message': 'User not logged in'})




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
