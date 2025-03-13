from typing import Dict, List, Any
import re
from transformers import pipeline

class DocumentClassifier:
    def __init__(self):
        # Load zero-shot classification pipeline
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
        # Define document types
        self.document_types = [
            "invoice", 
            "contract", 
            "report", 
            "email", 
            "resume", 
            "presentation",
            "memo",
            "financial_statement",
            "legal_notice"
        ]
        
        # Define priority levels
        self.priority_levels = [
            "urgent", 
            "high", 
            "medium", 
            "low"
        ]
    
    def classify_document_type(self, text: str) -> Dict[str, Any]:
        """
        Classify document type using zero-shot classification.
        
        Args:
            text: Document text
            
        Returns:
            Classification results with confidence scores
        """
        # For very long documents, use first 1024 tokens for classification
        text_sample = " ".join(text.split()[:1024])
        
        # Run zero-shot classification
        result = self.classifier(
            text_sample,
            candidate_labels=self.document_types,
            hypothesis_template="This document is a {}."
        )
        
        return {
            "document_type": result["labels"][0],
            "confidence": result["scores"][0],
            "all_types": [
                {"type": label, "score": score} 
                for label, score in zip(result["labels"], result["scores"])
            ]
        }
    
    def determine_priority(self, text: str) -> Dict[str, Any]:
        """
        Determine document priority using keyword matching and zero-shot classification.
        
        Args:
            text: Document text
            
        Returns:
            Priority assessment
        """
        # Look for explicit urgency indicators
        urgent_terms = ["urgent", "asap", "immediately", "emergency", "deadline", "critical"]
        text_lower = text.lower()
        explicit_urgency = any(term in text_lower for term in urgent_terms)
        
        # Check for dates and deadlines
        date_pattern = r'\b(today|tomorrow|next week|due by|due date|deadline)\b'
        contains_deadline = bool(re.search(date_pattern, text_lower))
        
        # Use zero-shot classification for priority
        text_sample = " ".join(text.split()[:1024])
        priority_result = self.classifier(
            text_sample,
            candidate_labels=self.priority_levels,
            hypothesis_template="This document has {} priority."
        )
        
        # Determine final priority
        # If explicit urgency indicators found, boost priority
        final_priority = priority_result["labels"][0]
        if explicit_urgency and final_priority not in ["urgent", "high"]:
            final_priority = "high"
        
        return {
            "priority": final_priority,
            "confidence": priority_result["scores"][0],
            "contains_explicit_urgency": explicit_urgency,
            "contains_deadline": contains_deadline,
            "all_priorities": [
                {"priority": label, "score": score} 
                for label, score in zip(priority_result["labels"], priority_result["scores"])
            ]
        }
    
    def classify_document(self, text: str) -> Dict[str, Any]:
        """
        Full document classification including type and priority.
        
        Args:
            text: Document text
            
        Returns:
            Complete classification results
        """
        type_result = self.classify_document_type(text)
        priority_result = self.determine_priority(text)
        
        return {
            "document_type": type_result["document_type"],
            "type_confidence": type_result["confidence"],
            "all_types": type_result["all_types"],
            "priority": priority_result["priority"],
            "priority_confidence": priority_result["confidence"],
            "urgency_indicators": {
                "explicit_terms": priority_result["contains_explicit_urgency"],
                "deadlines": priority_result["contains_deadline"]
            }
        }