from fastapi import UploadFile
import pytest
from app import app ,uploaded_data
import pandas as pd


async def test_upload_csv_success(mocker):
  # Mock the reading process
  mock_read = mocker.patch.object(UploadFile, 'read')
  mock_read.return_value = b'valid,csv,data'

  # Upload the file
  response = await app.post("/upload", files={"file": mocker.Mock(name="file")})

  # Assert successful upload
  assert response.status_code == 200
  assert response.json() == {"message": "File uploaded successfully", "file_id": mocker.ANY}

async def test_upload_csv_empty_file(mocker):
  # Mock the reading process to return empty data
  mock_read = mocker.patch.object(UploadFile, 'read')
  mock_read.return_value = b''

  # Upload the file
  response = await app.post("/upload", files={"file": mocker.Mock(name="file")})

  # Assert error for empty file
  assert response.status_code == 422
  assert "Empty file uploaded" in response.text  # Modify error message as needed

async def test_upload_csv_invalid_file(mocker):
  # Mock the reading process to return non-CSV data
  mock_read = mocker.patch.object(UploadFile, 'read')
  mock_read.return_value = b'This is not CSV data'

  # Upload the file
  response = await app.post("/upload", files={"file": mocker.Mock(name="file")})

  # Assert error for invalid file format
  assert response.status_code == 422
  assert "Invalid file format" in response.text  # Modify error message as needed

async def test_get_summary_success(mocker):
  # Mock uploaded data with a DataFrame
  file_id = "test_id"
  df = pd.DataFrame({"col1": [1, 2, 3]})
  mocker.patch.dict(uploaded_data, {file_id: df})

  # Get summary
  response = await app.get(f"/summary/{file_id}")

  # Assert successful retrieval
  assert response.status_code == 200
  assert response.json()["summary"]

async def test_get_summary_invalid_id():
  # Get summary with invalid ID
  response = await app.get("/summary/invalid_id")

  # Assert error for invalid ID
  assert response.status_code == 404
  assert "Invalid file ID!" in response.text
 
async def test_transform_data_success(mocker):
  # Mock uploaded data with a DataFrame
  file_id = "test_id"
  df = pd.DataFrame({"col1": [1, 2, 3]})
  mocker.patch.dict(uploaded_data, {file_id: df.copy()})

  # Define transformation data
  transform_data = {"transformation": "min_max_scaling"}

  # Apply transformation
  response = await app.post(f"/transform/{file_id}", json=transform_data)

  # Assert successful transformation
  assert response.status_code == 200
  assert response.json()["message"] == "Transformations applied successfully"

async def test_transform_data_invalid_id():
  # Apply transformation with invalid ID
  transform_data = {"transformation": "min_max_scaling"}
  response = await app.post("/transform/invalid_id", json=transform_data)

  # Assert error for invalid ID
  assert response.status_code == 404
  assert "Invalid file ID!" in response.text

async def test_transform_data_invalid_transformation(mocker):
  # Mock uploaded data with a DataFrame
  file_id = "test_id"
  df = pd.DataFrame({"col1": [1, 2, 3]})
  mocker.patch.dict(uploaded_data, {file_id: df.copy()})

  # Define invalid transformation data
  transform_data = {"transformation": "invalid_transformation"}
