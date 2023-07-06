from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import json,csv
import yaml
import os
import time
import csv   
import pandas as pd
from sqlalchemy.orm import Session
from model import FileData, CsvData
from config import SessionLocal


router = APIRouter()

Base_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(Base_DIR, "uploads")

timestr = time.strftime("%Y%m%d-%H%M%S")

@router.post("/upload")
async def upload_json(file: UploadFile):
    if file.content_type != "application/json":
        raise HTTPException(400, detail="INVALID DOCUMENT TYPE")

    content = await file.read()
    json_data = json.loads(content)

    # Create a new FileData object to store the file data
    file_data = FileData(filename=file.filename, content=json_data)

    # Open a new database session
    db = SessionLocal()

    try:
        # Add the file data to the session
        db.add(file_data)
        db.commit()
        db.refresh(file_data)
    finally:
        # Close the session
        db.close()

    return {"content": json_data, "filename": file.filename}


@router.post("/uploadndownload")
async def upload_n_downloadfile(file: UploadFile):
    """RETURN A YAML FILE FOR THE UPLOADED JSON FILE """
    if file.content_type != "application/json":
        raise HTTPException(400, detail="INVALID DOCUMENT TYPE")
    else:
        json_data = json.loads(file.file.read())
        new_filename = "{}_{}.yaml".format(os.path.splitext(file.filename)[0], timestr)

        SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_filename)
        with open(SAVE_FILE_PATH, "w") as f:
            yaml.dump(json_data, f)

        return FileResponse(
            path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=new_filename
        )



@router.post("/uploadcsv")
async def upload_csv(file: UploadFile):
    print("Upload CSV endpoint reached")
    if file.content_type != "text/csv":
        print("Invalid content type:", file.content_type) 
        raise HTTPException(400, detail="INVALID DOCUMENT TYPE")

    # Read the CSV file using pandas
    df = pd.read_csv(file.file)

    # Convert DataFrame to a list of dictionaries
    csv_data = df.to_dict(orient="records")

    # Open a new database session
    db = SessionLocal()

    try:
        # Create a new CsvData object for each row in the CSV data and add them to the session
        for row in csv_data:
            csv_row_data = CsvData(filename=file.filename, content=row)
            db.add(csv_row_data)

        # Commit the changes and refresh the objects
        db.commit()
        db.refresh(csv_row_data)
    finally:
        # Close the session
        db.close()

    return {"filename": file.filename}

@router.get("/downloadcsv/{csv_id}")
async def download_csv(csv_id: int):
    # Retrieve the CsvData object from the database
    db = SessionLocal()
    csv_data = db.query(CsvData).filter(CsvData.id == csv_id).first()
    db.close()

    if not csv_data:
        raise HTTPException(404, detail="CSV not found")

    # Generate a new filename for the downloaded file
    new_filename = "{}_{}.csv".format(os.path.splitext(csv_data.filename)[0], timestr)

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_filename)

    # Write the CSV content to the file
    with open(SAVE_FILE_PATH, "w") as f:
        f.write(csv_data.content)

    return FileResponse(
        path=SAVE_FILE_PATH,
        media_type="text/csv",
        filename=new_filename
    )


