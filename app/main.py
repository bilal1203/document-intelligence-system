from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Document Intelligence System",
    description="NLP-powered document processing API",
    version="0.1.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Document Intelligence System API"}

@app.post("/extract")
async def extract_entities(file: UploadFile = File(...)):
    """Extract named entities from a document"""
    # Will implement actual extraction logic later
    return {"status": "received", "filename": file.filename, "entities": []}

@app.post("/classify")
async def classify_document(file: UploadFile = File(...)):
    """Classify document type and priority"""
    # Will implement actual classification logic later
    return {"status": "received", "filename": file.filename, "type": "unknown"}

@app.post("/summarize")
async def summarize_document(file: UploadFile = File(...)):
    """Generate a summary of the document"""
    # Will implement actual summarization logic later
    return {"status": "received", "filename": file.filename, "summary": ""}

@app.post("/process")
async def process_document(file: UploadFile = File(...)):
    """Process document with all available functions"""
    # Will implement full processing pipeline later
    return {
        "status": "received",
        "filename": file.filename,
        "entities": [],
        "type": "unknown",
        "summary": "",
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)