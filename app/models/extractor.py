from typing import Dict, List, Tuple, Any
import spacy
from transformers import pipeline

class EntityExtractor:
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Load Hugging Face transformer for NER
        self.transformer_ner = pipeline(
            "token-classification",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple"
        )
    
    def extract_entities_spacy(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities using spaCy.
        
        Args:
            text: Document text
            
        Returns:
            List of extracted entities with type and position
        """
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
        
        return entities
    
    def extract_entities_transformer(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities using Hugging Face transformers.
        
        Args:
            text: Document text
            
        Returns:
            List of extracted entities with type and position
        """
        # For longer texts, we need to process in chunks
        max_length = 512
        text_chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        
        all_entities = []
        offset = 0
        
        for chunk in text_chunks:
            # Get predictions from transformer model
            results = self.transformer_ner(chunk)
            
            # Adjust positions based on chunk offset
            for entity in results:
                entity["start"] += offset
                entity["end"] += offset
                all_entities.append(entity)
            
            offset += len(chunk)
        
        return all_entities
    
    def extract_key_information(self, text: str) -> Dict[str, Any]:
        """
        Extract key business information like dates, amounts, names, etc.
        
        Args:
            text: Document text
            
        Returns:
            Dictionary with categorized entities
        """
        # Get entities from both models
        spacy_entities = self.extract_entities_spacy(text)
        transformer_entities = self.extract_entities_transformer(text)
        
        # Categorize and structure the information
        result = {
            "people": [],
            "organizations": [],
            "dates": [],
            "monetary_values": [],
            "locations": [],
            "other_entities": []
        }
        
        # Process spaCy entities
        for entity in spacy_entities:
            if entity["label"] == "PERSON":
                result["people"].append(entity)
            elif entity["label"] == "ORG":
                result["organizations"].append(entity)
            elif entity["label"] == "DATE":
                result["dates"].append(entity)
            elif entity["label"] == "MONEY":
                result["monetary_values"].append(entity)
            elif entity["label"] == "GPE" or entity["label"] == "LOC":
                result["locations"].append(entity)
            else:
                result["other_entities"].append(entity)
        
        # Add transformer entities that might have been missed
        for entity in transformer_entities:
            if entity["entity_group"] == "PER":
                # Check if already present in people
                if not any(e["text"] == entity["word"] for e in result["people"]):
                    result["people"].append({
                        "text": entity["word"],
                        "label": "PERSON",
                        "start": entity["start"],
                        "end": entity["end"],
                        "source": "transformer"
                    })
            elif entity["entity_group"] == "ORG":
                if not any(e["text"] == entity["word"] for e in result["organizations"]):
                    result["organizations"].append({
                        "text": entity["word"],
                        "label": "ORG",
                        "start": entity["start"],
                        "end": entity["end"],
                        "source": "transformer"
                    })
            elif entity["entity_group"] == "LOC":
                if not any(e["text"] == entity["word"] for e in result["locations"]):
                    result["locations"].append({
                        "text": entity["word"],
                        "label": "LOC",
                        "start": entity["start"],
                        "end": entity["end"],
                        "source": "transformer"
                    })
        
        return result