import os
from typing import Dict, Optional, List, Tuple
import PyPDF2
import docx

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
    with open(file_path, "r", encoding="utf-8") as file:
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

async def save_upload_file(upload_file, destination: str) -> str:
    """
    Save an uploaded file to the specified destination.
    
    Args:
        upload_file: FastAPI UploadFile object
        destination: Directory to save the file
        
    Returns:
        Path to the saved file
    """
    os.makedirs(destination, exist_ok=True)
    file_path = os.path.join(destination, upload_file.filename)
    
    with open(file_path, "wb") as buffer:
        content = await upload_file.read()
        buffer.write(content)
    
    return file_path