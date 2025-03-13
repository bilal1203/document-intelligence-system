import os
import sys
import unittest
from pathlib import Path

# Add the parent directory to the path so we can import the app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.extractor import EntityExtractor
from app.models.classifier import DocumentClassifier
from app.models.summarizer import DocumentSummarizer

class TestDocumentProcessing(unittest.TestCase):
    def setUp(self):
        self.extractor = EntityExtractor()
        self.classifier = DocumentClassifier()
        self.summarizer = DocumentSummarizer()
        
        # Sample texts for testing
        self.contract_text = """
        CONTRACT AGREEMENT
        
        This agreement is made on January 15, 2023, between ABC Corporation, located at 123 Business Avenue, New York, NY, and XYZ Ltd., located at 456 Commerce Street, San Francisco, CA.
        
        The parties agree to the following terms:
        
        1. ABC Corporation will provide consulting services to XYZ Ltd. for a period of 12 months.
        2. XYZ Ltd. will pay $5,000 per month for these services.
        3. This agreement can be terminated with 30 days notice by either party.
        
        Signed,
        
        John Smith, CEO
        ABC Corporation
        
        Jane Doe, President
        XYZ Ltd.
        """
        
        self.email_text = """
        From: john.smith@example.com
        To: jane.doe@company.com
        Subject: Urgent: Meeting Tomorrow
        
        Hi Jane,
        
        I hope this email finds you well. I'm writing to remind you about our important meeting tomorrow at 10:00 AM. We need to discuss the quarterly results and the new product launch.
        
        Please bring your presentation and the market analysis report. Bob from Marketing and Sarah from Finance will also join us.
        
        Best regards,
        John Smith
        VP of Operations
        Phone: (555) 123-4567
        """
    
    def test_entity_extraction(self):
        """Test entity extraction functionality"""
        contract_entities = self.extractor.extract_key_information(self.contract_text)
        
        # Basic validation
        self.assertTrue(len(contract_entities["people"]) > 0, "Should extract people")
        self.assertTrue(len(contract_entities["organizations"]) > 0, "Should extract organizations")
        self.assertTrue(len(contract_entities["dates"]) > 0, "Should extract dates")
        self.assertTrue(len(contract_entities["monetary_values"]) > 0, "Should extract monetary values")
        
        # Specific validation
        org_names = [org["text"].lower() for org in contract_entities["organizations"]]
        self.assertTrue(any("abc" in name for name in org_names), "Should find ABC Corporation")
        self.assertTrue(any("xyz" in name for name in org_names), "Should find XYZ Ltd")
        
    def test_document_classification(self):
        """Test document classification functionality"""
        contract_classification = self.classifier.classify_document(self.contract_text)
        email_classification = self.classifier.classify_document(self.email_text)
        
        # Verify contract is classified correctly
        self.assertEqual(contract_classification["document_type"], "contract", 
                         "Should classify as contract")
        
        # Verify email is classified correctly
        self.assertEqual(email_classification["document_type"], "email", 
                         "Should classify as email")
        
        # Verify priority for urgent email
        self.assertIn(email_classification["priority"], ["urgent", "high"], 
                      "Urgent email should be high priority")
    
    def test_document_summarization(self):
        """Test document summarization functionality"""
        contract_summary = self.summarizer.generate_summary(self.contract_text)
        email_summary = self.summarizer.generate_summary(self.email_text)
        
        # Verify summaries are generated
        self.assertTrue(len(contract_summary["summary"]) > 0, "Should generate contract summary")
        self.assertTrue(len(email_summary["summary"]) > 0, "Should generate email summary")
        
        # Verify summaries are shorter than original
        self.assertLess(contract_summary["summary_length"], len(self.contract_text.split()), 
                       "Summary should be shorter than original")
        self.assertLess(email_summary["summary_length"], len(self.email_text.split()), 
                       "Summary should be shorter than original")

if __name__ == "__main__":
    unittest.main()