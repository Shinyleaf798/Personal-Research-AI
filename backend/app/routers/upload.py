from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.rag import load_and_split, store_in_chroma
import os
import shutil
import hashlib

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory store for uploaded file hashes
# Prevents the same file from being uploaded twice
uploaded_hashes = set()

def get_file_hash(file_path: str) -> str:
    """
    Generate a unique MD5 hash for a file.
    Same file content will always produce the same hash.
    """
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Only accept PDF and TXT files
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

    # Save file temporarily to calculate hash
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Check for duplicate file using hash
    file_hash = get_file_hash(file_path)
    if file_hash in uploaded_hashes:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"File '{file.filename}' has already been uploaded.")

    # Store hash and process file
    uploaded_hashes.add(file_hash)
    chunks = load_and_split(file_path)
    store_in_chroma(chunks)
    os.remove(file_path)

    return {
        "message": f"File '{file.filename}' uploaded successfully",
        "chunks_stored": len(chunks)
    }