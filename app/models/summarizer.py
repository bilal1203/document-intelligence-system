from typing import Dict, List, Any
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class DocumentSummarizer:
    def __init__(self):
        # Load summarization pipeline
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )
    
    def chunk_text(self, text: str, max_chunk_size: int = 1024) -> List[str]:
        """
        Split text into chunks for processing by the summarizer.
        
        Args:
            text: Document text
            max_chunk_size: Maximum token count per chunk
            
        Returns:
            List of text chunks
        """
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            # Rough estimation of tokens (words)
            sentence_size = len(sentence.split())
            
            if current_size + sentence_size > max_chunk_size:
                # Current chunk is full, start a new one
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_size = sentence_size
            else:
                current_chunk.append(sentence)
                current_size += sentence_size
        
        # Add the last chunk if not empty
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def generate_summary(self, text: str, max_length: int = 150, min_length: int = 40) -> Dict[str, Any]:
        """
        Generate summary for document text.
        
        Args:
            text: Document text
            max_length: Maximum length of the summary
            min_length: Minimum length of the summary
            
        Returns:
            Dictionary with summary and metadata
        """
        # For short texts, adjust min_length
        text_length = len(text.split())
        if text_length < 100:
            min_length = min(20, text_length // 2)
            max_length = min(60, text_length)
        
        # Handle long documents by chunking
        if text_length > 1024:
            chunks = self.chunk_text(text)
            chunk_summaries = []
            
            for i, chunk in enumerate(chunks):
                # Skip very short chunks
                if len(chunk.split()) < 50:
                    continue
                    
                chunk_result = self.summarizer(
                    chunk, 
                    max_length=max(30, min(100, len(chunk.split()) // 4)),
                    min_length=min(20, len(chunk.split()) // 8),
                    do_sample=False
                )
                chunk_summaries.append(chunk_result[0]["summary_text"])
            
            # Combine chunk summaries and summarize again if needed
            combined_summary = " ".join(chunk_summaries)
            
            # If the combined summary is still long, summarize it again
            if len(combined_summary.split()) > max_length * 1.5:
                final_result = self.summarizer(
                    combined_summary,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                summary = final_result[0]["summary_text"]
            else:
                summary = combined_summary
        else:
            # For shorter documents, summarize directly
            result = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            summary = result[0]["summary_text"]
        
        return {
            "summary": summary,
            "original_length": text_length,
            "summary_length": len(summary.split()),
            "compression_ratio": len(summary.split()) / max(1, text_length)
        }