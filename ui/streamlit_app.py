import streamlit as st
import requests
import json
import pandas as pd
import os
from io import StringIO

# Set the API URL (change if deployed elsewhere)
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Document Intelligence System",
    page_icon="📄",
    layout="wide"
)

st.title("Document Intelligence System")
st.subheader("AI-powered document analysis")

# File uploader
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])

# Processing options
st.sidebar.title("Processing Options")
extract_entities = st.sidebar.checkbox("Extract Entities", value=True)
classify_document = st.sidebar.checkbox("Classify Document", value=True)
summarize_document = st.sidebar.checkbox("Summarize Document", value=True)

# Process button
process_clicked = st.sidebar.button("Process Document")

if uploaded_file is not None and process_clicked:
    st.info("Processing document... Please wait.")
    
    # Determine which endpoint to use based on selections
    if all([extract_entities, classify_document, summarize_document]):
        endpoint = f"{API_URL}/process"
    elif extract_entities and not classify_document and not summarize_document:
        endpoint = f"{API_URL}/extract"
    elif classify_document and not extract_entities and not summarize_document:
        endpoint = f"{API_URL}/classify"
    elif summarize_document and not extract_entities and not classify_document:
        endpoint = f"{API_URL}/summarize"
    else:
        endpoint = f"{API_URL}/process"
    
    # Make API request
    files = {"file": (uploaded_file.name, uploaded_file, "multipart/form-data")}
    
    try:
        response = requests.post(endpoint, files=files)
        if response.status_code == 200:
            result = response.json()
            
            # Create tabs for different results
            tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Classification", "Entities", "Raw JSON"])
            
            # Summary tab
            with tab1:
                if "summary" in result:
                    st.subheader("Document Summary")
                    st.write(result["summary"]["summary"])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Original Length", result["summary"]["original_length"])
                    with col2:
                        st.metric("Summary Length", result["summary"]["summary_length"])
                    with col3:
                        st.metric("Compression Ratio", f"{result['summary']['compression_ratio']:.2f}")
                else:
                    st.warning("Summary not available. Enable summarization option.")
            
            # Classification tab
            with tab2:
                if "classification" in result:
                    st.subheader("Document Classification")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Document Type", result["classification"]["document_type"].capitalize())
                        st.progress(result["classification"]["type_confidence"])
                        st.caption(f"Confidence: {result['classification']['type_confidence']:.2f}")
                    
                    with col2:
                        st.metric("Priority", result["classification"]["priority"].capitalize())
                        st.progress(result["classification"]["priority_confidence"])
                        st.caption(f"Confidence: {result['classification']['priority_confidence']:.2f}")
                    
                    # Show all document types with scores
                    if "all_types" in result["classification"]:
                        st.subheader("Document Type Scores")
                        type_data = pd.DataFrame(result["classification"]["all_types"])
                        st.bar_chart(type_data.set_index("type")["score"])
                else:
                    st.warning("Classification not available. Enable classification option.")
            
            # Entities tab
            with tab3:
                if "entities" in result:
                    st.subheader("Extracted Entities")
                    
                    # Define entity categories and colors
                    entity_categories = {
                        "people": "🧑 People",
                        "organizations": "🏢 Organizations",
                        "dates": "📅 Dates",
                        "monetary_values": "💰 Money",
                        "locations": "📍 Locations",
                        "other_entities": "🔖 Other"
                    }
                    
                    # Create tabs for each entity type
                    entity_tabs = st.tabs(list(entity_categories.values()))
                    
                    # Display entities in each tab
                    for i, (key, label) in enumerate(entity_categories.items()):
                        with entity_tabs[i]:
                            if result["entities"][key] and len(result["entities"][key]) > 0:
                                # Create a dataframe for the entities
                                df = pd.DataFrame(result["entities"][key])
                                st.dataframe(df)
                            else:
                                st.info(f"No {key.replace('_', ' ')} found in the document.")
                else:
                    st.warning("Entities not available. Enable entity extraction option.")
            
            # Raw JSON tab
            with tab4:
                st.subheader("Raw API Response")
                st.json(result)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
else:
    if process_clicked:
        st.warning("Please upload a document first.")
    else:
        st.info("Upload a document and select processing options to begin.")

# About section
st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.info(
    """
    This application uses NLP and AI to analyze documents, extract key information, classify document types, and generate summaries.
    
    Powered by Hugging Face transformers and spaCy.
    """
)