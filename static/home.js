document.addEventListener("alpine:init", () => {
    Alpine.data("appData", () => {
        return {
            title: "Decision Support System",
            BaseUrl: "http://127.0.0.1:5000",
            version: '1.0',
            isDatasetLoaded: false,
            isDataAnalysis: false,
            isPredictionSuccess: false,
            isTryAgainVisible: false,
            marketingAvenue: '',
            budgetAmount: '',
            predictedSales: '',
            datasetProperties: null,
            chartData: null,
            analysisResults: '', // Define analysisResults
            // datasetPath: '{{ session("dataset_path") }}',

            loadDataset() {
                // Get the input element
                const fileInput = document.getElementById('dataset-file');

                // Check if a file is selected
                if (fileInput.files.length > 0) {
                    // Get the selected file
                    const file = fileInput.files[0];

                    // Create a new FormData object
                    const formData = new FormData();
                    formData.append('file', file); // 'file' should match the name attribute in your form

                    // Send the FormData object using Axios
                    axios.post('/load_dataset', formData)
                        .then(function (response) {
                            console.log(response.data); // Log the response data for debugging
                        })
                        .catch(function (error) {
                            console.error(error); // Log any errors
                        });
                } else {
                    console.log('No file selected.');
                }
            },

            dataAnalysis() {
                const apiUrl = "/data_trend_analysis"; // Replace with your actual server route
                axios.get(apiUrl)
                    .then((response) => {
                        // Assuming that `response.data` contains the chart data
                        this.chartData = response.data;

                        // Log chart data for debugging
                        console.log(`Chart Data:`, this.chartData);

                        // Create and update the chart image
                        this.updateChartImage();
                        // Display data trend analysis results
                        this.displayRecommendations();
                        this.isDataAnalysis = true;
                    })
                    .catch((error) => {
                        console.error('Error performing data trend analysis:', error);
                    });
            },
            displayRecommendations() {
                // Assuming you have the hard-coded values
                const correlationData = {
                    'TV': 0.7,
                    'Radio': 0.5,
                    'Social Media': 0.6
                };
            
                const highestSalesAvenue = 'TV';
                const leastSalesAvenue = 'Radio';
                const averageSales = 50000;
                const budgetAmount = 10000;
            
                const recommendationsContainer = document.getElementById('recommendations-container');
                recommendationsContainer.innerHTML = `
                    <h2>Recommendations</h2>
                    <p>Based on the data analysis, allocate your budget to the marketing avenue with the highest positive correlation with Sales.</p>
                    <p>Here are the correlations:</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Marketing Avenue</th>
                                <th>Correlation</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>TV</td>
                                <td>${correlationData.TV}</td>
                            </tr>
                            <tr>
                                <td>Radio</td>
                                <td>${correlationData.Radio}</td>
                            </tr>
                            <tr>
                                <td>Social Media</td>
                                <td>${correlationData['Social Media']}</td>
                            </tr>
                        </tbody>
                    </table>
                    <h2>Data Trend Analysis Results</h2>
                    <p>Highest Sales Marketing Avenue: ${highestSalesAvenue}</p>
                    <p>Least Sales Marketing Avenue: ${leastSalesAvenue}</p>
                    <p>Average Sales: ${averageSales}</p>
                    <p>Budget Amount: ${budgetAmount}</p>
                `;
            },
            
            showCorrelationImage() {
                const chartImage = document.getElementById('chart-image');
                chartImage.style.display = 'block'; // Display the image
            },


            updateChartImage() {
                if (this.chartData.correlation_chart_image) {
                    const chartImage = document.getElementById('chart-image');
                    chartImage.src = `data:image/png;base64,${this.chartData.correlation_chart_image}`;
                }
            },

            createBarChart() {
                if (this.chartData) {
                    // Extract data for the chart
                    const labels = Object.keys(this.chartData);
                    const values = Object.values(this.chartData);

                    // Remove any existing canvas
                    const existingCanvas = document.getElementById('chartCanvas');
                    if (existingCanvas) {
                        existingCanvas.parentNode.removeChild(existingCanvas);
                    }

                    // Create a new canvas element for the chart
                    const canvas = document.createElement('canvas');
                    canvas.id = 'chartCanvas'; // Set the canvas ID
                    const chartContainer = document.getElementById('chart-container');
                    chartContainer.appendChild(canvas);

                    // Get the context for the canvas
                    const ctx = canvas.getContext('2d');
                    canvas.width = 400;
                    canvas.height = 300;

                    // Create the bar chart using Chart.js
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [
                                {
                                    label: 'Sales vs. Marketing Avenues',
                                    data: values,
                                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 1,
                                },
                            ],
                        },
                        options: {
                            scales: {
                                y: {
                                    beginAtZero: true,
                                },
                            },
                        },
                    });
                }
            },


            viewProperties() {
                axios.get('/view_properties')
                    .then(function (response) {
                        const datasetProperties = response.data;
                        // Extract data and update the HTML to display the results
                        const numRows = datasetProperties.num_rows;
                        const numColumns = datasetProperties.num_columns;
                        const columnNames = datasetProperties.column_names;
                        const firstFewRows = datasetProperties.first_few_rows;

                        // Update the HTML to display the results in a table-like format
                        const resultContainer = document.getElementById('result-container');
                        resultContainer.innerHTML = `
                            <h3>Dataset Properties:</h3>
                            <p>Number of Rows: ${numRows}</p>
                            <p>Number of Columns: ${numColumns}</p>
                            <h4>Column Names:</h4>
                            <ul>${columnNames.map(column => `<li>${column}</li>`).join('')}</ul>
                            <h4>First Few Rows:</h4>
                            <table>
                                <thead>
                                    <tr>${columnNames.map(column => `<th>${column}</th>`).join('')}</tr>
                                </thead>
                                <tbody>
                                    ${firstFewRows.map(row => `<tr>${columnNames.map(column => `<td>${row[column]}</td>`).join('')}</tr>`).join('')}
                                </tbody>
                            </table>
                        `;
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            },

            predictSales() {
                // Assuming you have the prediction logic implemented on the server
                const predictionData = {
                    marketingAvenue: this.marketingAvenue,
                    budgetAmount: this.budgetAmount,
                };

                axios.post('/predict_sales', predictionData, { data: predictionData, dataset: 'static/files/uploaded_dataset.csv' }) // Pass the dataset path)
                    .then((response) => {
                        console.log(response); // Add this line to log the response
                        if (response.data.hasOwnProperty('predicted_sales')) {
                            this.predictedSales = `Predicted Sales: $${response.data.predicted_sales} for ${response.data.marketing_avenue}`;
                        } else {
                            this.predictedSales = ''; // Clear any previous result
                            const errorMessage = document.getElementById('errorMessage');
                            errorMessage.textContent = 'Error: Predicted sales could not be calculated.';
                            errorMessage.style.display = 'block';
                            console.error('Error predicting sales:', response.data.error);
                            this.predictedSales = `Error: ${response.data.error}`;

                            // Hide the error message after 1 minute (60000 milliseconds)
                            setTimeout(() => {
                                errorMessage.style.display = 'none';
                            }, 60000);
                        }
                    })
                    .catch((error) => {
                        console.error('Error predicting sales:', error);
                        this.predictedSales = `Error: ${error.message}`;
                    });
            },



            getDataTrendAnalysis() {
                axios.get('/data_trend_analysis')
                    .then((response) => {
                        this.tvCorrelation = response.data.correlation_sales_tv;
                        this.radioCorrelation = response.data.correlation_sales_radio;
                        this.socialMediaCorrelation = response.data.correlation_sales_social_media;
                    })
                    .catch((error) => {
                        console.error('Error fetching data trend analysis:', error);
                    });
            },

            getPredictiveAnalysis() {
                axios.get('/predictive_analysis')
                    .then((response) => {
                        this.marketingAvenue = response.data.marketingAvenue;
                        this.budgetAmount = response.data.budgetAmount;
                        this.predictedSales = response.data.predictedSales;
                    })
                    .catch((error) => {
                        console.error('Error fetching predictive analysis:', error);
                    });
            },



            retryLoad() {
                axios.post('/load_dataset', {})
                    .then((response) => {
                        if (response.data.success) {
                            this.showSuccessMessage('Dataset loaded successfully!');
                        } else {
                            this.showErrorMessage('Failed to load dataset. Please retry.');
                        }
                    })
                    .catch((error) => {
                        this.showErrorMessage('Failed to load dataset. Please retry.');
                    });
            },

            showSuccessMessage(message) {
                console.log('Success:', message);
            },

            showErrorMessage(message) {
                console.error('Error:', message);
            },
        };
    });

});
