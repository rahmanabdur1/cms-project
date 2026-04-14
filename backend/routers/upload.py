from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "static/uploads")
MAX_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "audio/mpeg",
    "audio/wav",
    "audio/ogg",
    "video/mp4",
    "video/webm",
    "video/ogg",
}


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file.content_type}' is not allowed.",
        )

    contents = await file.read()

    if len(contents) > MAX_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the {MAX_MB}MB limit.",
        )

    ext = file.filename.split(".")[-1].lower() if "." in file.filename else "bin"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(contents)

    return JSONResponse({
        "url": f"/static/uploads/{filename}",
        "filename": filename,
        "size_bytes": len(contents),
        "content_type": file.content_type,
    })


@router.delete("/{filename}")
def delete_file(filename: str):
    # Prevent path traversal attacks
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid filename.")

    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found.")

    os.remove(filepath)
    return {"message": "File deleted successfully", "filename": filename}


@router.get("/list")
def list_files():
    try:
        files = os.listdir(UPLOAD_DIR)
        files = [f for f in files if not f.startswith(".")]
        return {"files": files, "count": len(files)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))