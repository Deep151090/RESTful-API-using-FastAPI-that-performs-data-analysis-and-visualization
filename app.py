import io
from fastapi import Body, FastAPI, Query, UploadFile, File,Response
import uuid
import pandas as pd
from matplotlib import pyplot as plt
import base64  # for base64 encoding image data
from pydantic import BaseModel


app = FastAPI()
global uploaded_data
# In-memory storage for uploaded data (replace with database if needed)
uploaded_data = {}

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
  
  # Read the uploaded file content
  content = await file.read()
  
  # Generate a unique file identifier
  file_id = str(uuid.uuid4())
  # Load the content into a Pandas DataFrame
  df = pd.read_csv(io.BytesIO(content))
  # Store the DataFrame with the file_id as key
  uploaded_data[file_id] = df
  return {"message": "File uploaded successfully", "file_id": file_id}
 
@app.get("/summary/{file_id}")
async def get_summary(file_id: str):
 
  if file_id not in uploaded_data:
      return {"message": "Invalid file ID!"}
  
  df = uploaded_data[file_id]
  
  # Get summary statistics from the DataFrame
  summary = df.describe().to_dict()
  
  # Include data types of each column
  summary.update({"dtypes": df.dtypes.to_dict()})
  
  return {"summary" : str(summary)}
  

class Transform_data(BaseModel):
    transformation: str
    normalize: list[str] = None  # List of columns for normalization
    fill_missing: dict[str, float | int] = None  # Dictionary for specific column-value imputation
    
@app.post("/transform/{file_id}")
async def transform_data(file_id: str, data: Transform_data = Body(...)):
  #global uploaded_data
  if file_id not in uploaded_data:
      return {"message": "Invalid file ID!"}
  df = uploaded_data[file_id]
  

  df_min_max_scaled = df.copy() 

   
# apply normalization techniques 
  for column in df_min_max_scaled.columns: 
    df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
  
  

  # Generate a new unique file_id for the transformed data 
  new_file_id = str(uuid.uuid4())
  uploaded_data[new_file_id] = df_min_max_scaled.copy()
  
  return {"message": "Transformations applied successfully", "file_id": new_file_id}

@app.get("/visualize/{new_file_id}")
async def visualize_data(new_file_id: str, column: str = Query("data", description="Column name for histogram")):
    # Read CSV data from specified path
    if new_file_id not in uploaded_data:
      return {"message": "Invalid file ID!"}
  
    df = uploaded_data[new_file_id]
    print(df)
    # Generate histogram
    df.hist(by='students_no', figsize=[12, 8], bins=15)
    plt.show()
    

   
    return {"message": "Histogram generated successfully!"}
    

