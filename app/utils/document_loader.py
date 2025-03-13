import os
import tempfile
from typing import Dict, Optional, List, Tuple
import PyPDF2
import docx
from fastapi import UploadFile

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text content from a PDF file."""
    text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Extract text content from a DOCX file."""
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(file_path: str) -> str:
    """Extract text content from a TXT file."""
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        text = file.read()
    return text

def load_document(file_path: str) -> Tuple[str, str]:
    """
    Load document and extract text based on file extension.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        Tuple containing (extracted_text, file_extension)
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    
    if file_extension == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        text = extract_text_from_docx(file_path)
    elif file_extension == ".txt":
        text = extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")
    
    return text, file_extension

async def process_uploaded_file(upload_file: UploadFile) -> Tuple[str, str]:
    """
    Process an uploaded file and extract its text content.
    
    Args:
        upload_file: FastAPI UploadFile object
        
    Returns:
        Tuple containing (extracted_text, file_extension)
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(upload_file.filename)[1]) as temp:
        # Read uploaded file content
        content = await upload_file.read()
        # Write to temporary file
        temp.write(content)
        temp_path = temp.name
    
    try:
        # Extract text from the temporary file
        text, extension = load_document(temp_path)
        return text, extension
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)