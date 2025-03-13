# Document Intelligence System

An NLP-powered document processing system that can extract entities, classify documents, and generate summaries.

## Features

- **Entity Extraction**: Identify people, organizations, dates, monetary values, and locations in documents
- **Document Classification**: Categorize documents by type (e.g., invoice, contract, email) and priority
- **Document Summarization**: Generate concise summaries of document content
- **Multi-format Support**: Process PDF, DOCX, and TXT files
- **API & UI**: RESTful API with FastAPI and user-friendly Streamlit interface

## Architecture

The system is built with a modular architecture:

- **FastAPI Backend**: Provides RESTful endpoints for document processing
- **ML Components**: Uses Hugging Face transformers and spaCy for NLP tasks
- **Streamlit UI**: Simple and intuitive user interface
- **Docker Support**: Easy deployment with containerization

## Installation

### Option 1: Local Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/document-intelligence-system.git
   cd document-intelligence-system
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Download required models:
   ```
   python -m spacy download en_core_web_sm
   python -c "import nltk; nltk.download('punkt')"
   ```

4. Run the API server:
   ```
   uvicorn app.main:app --reload
   ```

5. In a separate terminal, run the UI:
   ```
   streamlit run ui/streamlit_app.py
   ```

### Option 2: Docker Deployment

1. Build and run using Docker Compose:
   ```
   docker-compose up --build
   ```

2. Access the applications:
   - API: http://localhost:8000
   - UI: http://localhost:8501

## API Endpoints

- `POST /extract`: Extract named entities from a document
- `POST /classify`: Classify document type and priority
- `POST /summarize`: Generate a summary of the document
- `POST /process`: Process a document with all available functions

## Usage

1. Access the Streamlit UI at http://localhost:8501
2. Upload a document (PDF, DOCX, or TXT)
3. Select the processing options you want
4. Click "Process Document"
5. View the results in the interface

## Testing

Run the test suite:
```
python -m unittest discover tests
```

## License

MIT