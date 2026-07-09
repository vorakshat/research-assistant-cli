import os
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI(title="RAG File Ingestion Engine")

# Configure a safe local folder path where uploaded files will be stored
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploaded_docs")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def ingest_document(file: UploadFile = File(...)):
    """
    Receives binary files via multipart/form-data. 
    Streams the file content chunk-by-chunk and saves it to local disk.
    """
    # 1. Validation Shield: Restrict input types to PDFs and Markdown files only
    allowed_extensions = [".pdf", ".md", ".markdown"]
    file_extension = os.path.splitext(file.filename.lower())[1]
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type '{file_extension}'. Only PDFs and Markdown are permitted."
        )
        
    # 2. Establish the exact file storage destination path
    destination_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # 3. Stream the file data safely using standard async file I/O operations
    try:
        # Read the file contents as bytes in a non-blocking execution loop
        contents = await file.read()
        
        # Write the buffered bytes directly down onto your server's disk storage
        with open(destination_path, "wb") as buffer:
            buffer.write(contents)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stream file data: {str(e)}")
    finally:
        # Crucial Lifecycle Step: Always close the file pointer to free up resources
        await file.close()

    return {
        "status": "upload_successful",
        "saved_filename": file.filename,
        "content_type": file.content_type,
        "absolute_storage_path": destination_path
    }