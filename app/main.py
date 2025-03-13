from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any

from app.models.extractor import EntityExtractor
from app.models.classifier import DocumentClassifier
from app.models.summarizer import DocumentSummarizer
from app.utils.document_loader import process_uploaded_file

app = FastAPI(
    title="Document Intelligence System",
    description="NLP-powered document processing API",
    version="0.1.0",
)

# Initialize models
entity_extractor = EntityExtractor()
document_classifier = DocumentClassifier()
document_summarizer = DocumentSummarizer()

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
    try:
        # Process the uploaded file
        text, extension = await process_uploaded_file(file)
        
        # Extract entities
        entities = entity_extractor.extract_key_information(text)
        
        return {
            "status": "success",
            "filename": file.filename,
            "file_type": extension,
            "entities": entities
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/classify")
async def classify_document(file: UploadFile = File(...)):
    """Classify document type and priority"""
    try:
        # Process the uploaded file
        text, extension = await process_uploaded_file(file)
        
        # Classify document
        classification = document_classifier.classify_document(text)
        
        return {
            "status": "success",
            "filename": file.filename,
            "file_type": extension,
            "classification": classification
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error classifying document: {str(e)}")

@app.post("/summarize")
async def summarize_document(file: UploadFile = File(...)):
    """Generate a summary of the document"""
    try:
        # Process the uploaded file
        text, extension = await process_uploaded_file(file)
        
        # Generate summary
        summary = document_summarizer.generate_summary(text)
        
        return {
            "status": "success",
            "filename": file.filename,
            "file_type": extension,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing document: {str(e)}")

@app.post("/process")
async def process_document(file: UploadFile = File(...)):
    """Process document with all available functions"""
    try:
        # Process the uploaded file
        text, extension = await process_uploaded_file(file)
        
        # Run all processing functions
        entities = entity_extractor.extract_key_information(text)
        classification = document_classifier.classify_document(text)
        summary = document_summarizer.generate_summary(text)
        
        # Return combined results
        return {
            "status": "success",
            "filename": file.filename,
            "file_type": extension,
            "text_length": len(text.split()),
            "entities": entities,
            "classification": classification,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)