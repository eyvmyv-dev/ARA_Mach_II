"""
Text preprocessing and tokenization for equipment descriptions
"""
import re
from typing import List, Set
import string


class TextPreprocessor:
    """
    Text preprocessing for equipment classification
    """
    
    def __init__(self):
        # Common stop words for equipment descriptions
        self.stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'among', 'throughout', 'despite',
            'towards', 'upon', 'concerning', 'under', 'within', 'without', 'throughout'
        }
        
        # Equipment-specific terms to preserve
        self.preserve_terms = {
            'ahu', 'hvac', 'rtu', 'vav', 'fcu', 'uv', 'led', 'ac', 'dc',
            'rpm', 'cfm', 'btu', 'psi', 'gpm', 'kwh', 'amp', 'volt'
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text for processing
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize common separators
        text = re.sub(r'[/\\|]', ' ', text)
        
        # Handle equipment IDs (preserve alphanumeric with dots/dashes)
        text = re.sub(r'([a-z]+)\.([0-9]+)', r'\1 \2', text)
        text = re.sub(r'([a-z]+)-([0-9]+)', r'\1 \2', text)
        
        # Remove location prefixes that don't add value
        text = re.sub(r'^(t[0-9]+\.f[0-9]+[-\s]*)', '', text)
        text = re.sub(r'^(terminal\s+[0-9]+[,\s]*)', '', text)
        
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into meaningful tokens
        
        Args:
            text: Cleaned text to tokenize
            
        Returns:
            List of tokens
        """
        if not text:
            return []
        
        # Split on whitespace and punctuation (except preserved characters)
        tokens = re.findall(r'[a-zA-Z0-9]+(?:\.[0-9]+)?', text)
        
        # Filter tokens
        filtered_tokens = []
        for token in tokens:
            token = token.lower()
            
            # Skip very short tokens unless they're important abbreviations
            if len(token) < 2 and token not in self.preserve_terms:
                continue
            
            # Skip stop words unless they're equipment terms
            if token in self.stop_words and token not in self.preserve_terms:
                continue
            
            # Skip pure numbers unless they're equipment IDs
            if token.isdigit() and len(token) > 4:
                continue
            
            filtered_tokens.append(token)
        
        return filtered_tokens
    
    def extract_equipment_ids(self, text: str) -> List[str]:
        """
        Extract equipment identifiers from text
        
        Args:
            text: Text to extract IDs from
            
        Returns:
            List of equipment IDs found
        """
        ids = []
        
        # Pattern for AHU/RTU/FCU with numbers
        equipment_patterns = [
            r'(ahu\s*[#\-]?\s*[0-9]+(?:\.[0-9]+)?)',
            r'(rtu\s*[#\-]?\s*[0-9]+(?:\.[0-9]+)?)',
            r'(fcu\s*[#\-]?\s*[0-9]+(?:\.[0-9]+)?)',
            r'(pump\s*[#\-]?\s*[0-9a-z]+)',
            r'(chiller\s*[#\-]?\s*[0-9a-z]+)',
            r'(elevator\s*[#\-]?\s*[0-9]+)',
            r'(boiler\s*[#\-]?\s*[0-9a-z]+)'
        ]
        
        text_lower = text.lower()
        for pattern in equipment_patterns:
            matches = re.findall(pattern, text_lower)
            ids.extend(matches)
        
        return list(set(ids))  # Remove duplicates
    
    def normalize_equipment_type(self, equipment_type: str) -> str:
        """
        Normalize equipment type names for consistency
        
        Args:
            equipment_type: Raw equipment type
            
        Returns:
            Normalized equipment type
        """
        if not equipment_type:
            return "OTHER"
        
        # Mapping of common variations to standard names
        type_mappings = {
            'air handling unit': 'AHU',
            'air handler': 'AHU',
            'ahu': 'AHU',
            'rooftop unit': 'RTU',
            'rtu': 'RTU',
            'fan coil unit': 'FCU',
            'fcu': 'FCU',
            'chiller': 'CHILLER',
            'pump': 'PUMP',
            'elevator': 'ELEVATOR',
            'boiler': 'BOILER',
            'hvac': 'HVAC',
            'electrical': 'ELECTRICAL',
            'plumbing': 'PLUMBING',
            'security': 'SECURITY',
            'fire': 'FIRE_SAFETY'
        }
        
        normalized = equipment_type.lower().strip()
        return type_mappings.get(normalized, equipment_type.upper())