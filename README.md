This FastAPI application provides functionalities for uploading CSV data, obtaining summaries, applying transformations, and generating visualizations.

Dependencies:

fastapi: Web framework for building APIs (install with pip install fastapi)

uvicorn: ASGI server for running FastAPI applications (install with pip install uvicorn)

pandas: Data analysis and manipulation library (install with pip install pandas)

pydantic: Data validation library (install with pip install pydantic)

matplotlib: Visualization library for creating plots (install with pip install matplotlib)

Running the API:

Install dependencies:

Bash
pip install fastapi uvicorn pandas pydantic matplotlib


Run the application:

Bash
uvicorn app:app --reload  # Starts the API server in development mode with hot reload

we can then access the API documentation at http://localhost:8000/docs.

API Endpoints:

1. Upload CSV:

Method: POST
URL: http://localhost:8000/upload
Request Body: Multipart form-data with a file named "file" containing the CSV data.

Response:

JSON
{
  "message": "File uploaded successfully",
  "file_id": "some-unique-id"
}

message: Confirmation message for successful upload.
file_id: Unique identifier for the uploaded data, used in subsequent requests.

2. Get Summary:

Method: GET
URL: http://localhost:8000/summary/{file_id}
Path Parameters:
{file_id}: The unique ID obtained from uploading the CSV.
Response:

JSON
{
  "summary": {
    # Contains summary statistics of the uploaded data
  }
}

summary: Dictionary containing descriptive statistics (mean, standard deviation, etc.) for each column in the data.
3. Transform Data:

Method: POST
URL: http://localhost:8000/transform/{file_id}
Path Parameters:
{file_id}: The unique ID obtained from uploading the CSV.
Request Body: JSON data with the following structure:
JSON
{
  "transformation": "min_max_scaling",  # Supported transformation type
  "normalize": ["column1", "column2"],  # Optional list of columns to normalize
  "fill_missing": {"column3": 0}        # Optional dictionary for imputing missing values
}

 Type of transformation to apply (currently supports "min_max_scaling").

normalize: List of column names to normalize (min-max scaling).
fill_missing: Dictionary specifying values to impute for missing entries in specific columns.

Response:

JSON
{
  "message": "Transformations applied successfully",
  "file_id": "new_file_id"  # New ID for the transformed data
}

message: Confirmation message for successful transformation.
new_file_id: Unique identifier for the transformed data (different from the original upload ID).

4. Visualize Data:

Method: GET
URL: http://localhost:8000/visualize/{new_file_id}
Path Parameters:
{new_file_id}: The unique ID obtained from transforming the data.

Response:

JSON
{
  "message": "Histogram generated successfully!"
}

message: Confirmation message for successful histogram generation.
