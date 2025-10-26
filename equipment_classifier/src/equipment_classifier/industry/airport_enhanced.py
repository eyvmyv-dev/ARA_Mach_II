"""
Enhanced Airport-specific equipment classification patterns
Reads equipment classes from Equipment Classes.xlsx
"""
import os
import pandas as pd
import re
from typing import Dict, List, Optional
from .base import IndustryPatterns


class AirportPatterns(IndustryPatterns):
    """
    Airport-specific equipment patterns and classifications
    Dynamically loads equipment classes from Equipment Classes.xlsx
    """

    def __init__(self, equipment_classes_file: Optional[str] = None):
        super().__init__('AIRPORT')
        self.equipment_classes_file = equipment_classes_file or "Equipment Classes.xlsx"
        self.equipment_definitions = self._load_equipment_definitions()

    def _load_equipment_definitions(self) -> pd.DataFrame:
        """
        Load equipment class definitions from Excel file
        """
        try:
            # Try current directory first, then parent directories
            file_paths = [
                self.equipment_classes_file,
                f"../{self.equipment_classes_file}",
                f"../../{self.equipment_classes_file}"
            ]
            
            for file_path in file_paths:
                if os.path.exists(file_path):
                    df = pd.read_excel(file_path)
                    print(f"✅ Loaded equipment definitions from: {file_path}")
                    print(f"📋 Found {len(df)} equipment class definitions")
                    return df[['Class', 'Description']].dropna()
            
            # If file not found, use fallback
            print(f"⚠️ Equipment Classes file not found. Using basic patterns.")
            return self._create_fallback_definitions()
            
        except Exception as e:
            print(f"⚠️ Error loading Equipment Classes: {e}")
            return self._create_fallback_definitions()

    def _create_fallback_definitions(self) -> pd.DataFrame:
        """
        Fallback equipment definitions if Excel file not available
        """
        fallback_data = {
            'Class': ['AHU', 'RTU', 'BOILER', 'CHILL', 'PBB', 'AUPM'],
            'Description': [
                'Air Handler Unit',
                'Roof Top Unit', 
                'Boiler',
                'HVAC Chiller Systems',
                'Passenger Boarding Bridge',
                'Automated People Moving'
            ]
        }
        return pd.DataFrame(fallback_data)

    def _generate_patterns_from_description(self, class_code: str, description: str) -> List[str]:
        """
        Generate regex patterns based on equipment class and description
        """
        patterns = []
        
        # Always include the class code itself
        patterns.append(rf'\b{re.escape(class_code.lower())}\b')
        
        # Generate patterns based on description
        desc_lower = description.lower()
        
        # Special pattern mappings based on your equipment classes
        pattern_mappings = {
            'AHU': [
                r'\bahu\s*[#\-]?\s*[0-9]+(?:\.[0-9]+)?\b',
                r'\bair\s+handling\s+unit\b',
                r'\bair\s+handler\b'
            ],
            'RTU': [
                r'\brtu\s*[#\-]?\s*[0-9]+(?:\.[0-9]+)?\b', 
                r'\brooftop\s+unit\b',
                r'\broof\s+top\s+unit\b'
            ],
            'CHILL': [
                r'\bchiller\b',
                r'\bchilling\s+unit\b',
                r'\bchiller\s+room\b',
                r'\bchiller\s+pump\b'
            ],
            'BOILER': [
                r'\bboiler\b',
                r'\bboiler\s+room\b'
            ],
            'PBB': [
                r'\bjet\s*bridge\b',
                r'\bpassenger\s+boarding\s+bridge\b',
                r'\bbridge\b.*\bgate\b',
                r'\bgate\b.*\bbridge\b'
            ],
            'AUPM': [
                r'\belevator\b',
                r'\bescalator\b',
                r'\bmoving\s+walkway\b',
                r'\bpassenger\s+elevator\b'
            ],
            'BHS': [
                r'\bbaggage\b',
                r'\bconveyor\b',
                r'\bbaggage\s+handling\b'
            ],
            'CONVEYOR': [
                r'\bconveyor\b',
                r'\bbelt\s+conveyor\b'
            ],
            'DOORS': [
                r'\bdoor\b',
                r'\bdoors\b',
                r'\baccess\s+door\b'
            ],
            'EF': [
                r'\bexhaust\s+fan\b',
                r'\bfan\b.*\bexhaust\b'
            ],
            'EM': [
                r'\belectrical\s+meter\b',
                r'\belectric\s+meter\b',
                r'\bpower\s+meter\b'
            ],
            'EQUIPMEN': [
                r'\bequipment\b',
                r'\bgeneral\s+equipment\b'
            ],
            'GM': [
                r'\bgas\s+meter\b'
            ],
            'GPU': [
                r'\bground\s+power\b',
                r'\bpower\s+unit\b'
            ],
            'GSE': [
                r'\bground\s+support\b',
                r'\bground\s+equipment\b'
            ],
            'LAV': [
                r'\blavatory\b',
                r'\brestroom\b',
                r'\bwashroom\b'
            ],
            'PCA': [
                r'\bpreconditioned\s+air\b',
                r'\bpca\b'
            ],
            'PWSYS': [
                r'\bwater\s+system\b',
                r'\bpotable\s+water\b'
            ],
            'SAFETY': [
                r'\bfire\s+extinguisher\b',
                r'\bsafety\b',
                r'\bemergency\b'
            ],
            'VEH': [
                r'\bvehicle\b',
                r'\btruck\b',
                r'\bvan\b'
            ],
            'WM': [
                r'\bwater\s+meter\b'
            ]
        }
        
        # Use predefined patterns if available
        if class_code in pattern_mappings:
            patterns.extend(pattern_mappings[class_code])
        else:
            # Generate automatic patterns from description
            words = desc_lower.replace('-', ' ').split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    patterns.append(rf'\b{re.escape(word)}\b')
            
            # Try full description as phrase
            if len(words) > 1:
                phrase_pattern = r'\b' + r'\s+'.join([re.escape(w) for w in words]) + r'\b'
                patterns.append(phrase_pattern)
        
        return patterns

    def _load_patterns(self) -> Dict[str, List[str]]:
        """
        Load equipment patterns from Equipment Classes.xlsx
        """
        patterns = {}
        
        for _, row in self.equipment_definitions.iterrows():
            class_code = row['Class']
            description = row['Description'] 
            
            # Generate patterns for this equipment class
            class_patterns = self._generate_patterns_from_description(class_code, description)
            patterns[class_code] = class_patterns
        
        # Add catch-all patterns for common airport items not in main classes
        patterns.update({
            'OTHER': [
                r'\broom\b',
                r'\barea\b', 
                r'\boffice\b',
                r'\bparking\b'
            ]
        })
        
        return patterns

    def _load_synonyms(self) -> Dict[str, str]:
        """
        Load equipment synonyms/mappings from Equipment Classes.xlsx
        """
        synonyms = {}
        
        for _, row in self.equipment_definitions.iterrows():
            class_code = row['Class']
            description = row['Description'].lower()
            
            # Map common variations to official class codes
            synonym_mappings = {
                'chiller': 'CHILL',
                'air handler': 'AHU', 
                'air handling unit': 'AHU',
                'rooftop unit': 'RTU',
                'roof top unit': 'RTU',
                'elevator': 'AUPM',
                'escalator': 'AUPM', 
                'jet bridge': 'PBB',
                'passenger boarding bridge': 'PBB',
                'baggage': 'BHS',
                'conveyor': 'CONVEYOR',
                'exhaust fan': 'EF',
                'ground power': 'GPU',
                'lavatory': 'LAV',
                'restroom': 'LAV',
                'vehicle': 'VEH',
                'equipment': 'EQUIPMEN'
            }
            
            # Add description-based mappings
            for key, target in synonym_mappings.items():
                if key in description:
                    synonyms[key] = target
            
            # Add the class code itself
            synonyms[class_code.lower()] = class_code
        
        return synonyms

    def get_available_equipment_classes(self) -> List[str]:
        """
        Get list of all available equipment classes from Excel file
        """
        return sorted(self.equipment_definitions['Class'].tolist())
    
    def get_equipment_description(self, class_code: str) -> Optional[str]:
        """
        Get description for an equipment class code
        """
        match = self.equipment_definitions[self.equipment_definitions['Class'] == class_code]
        if not match.empty:
            return match.iloc[0]['Description']
        return None

    def add_custom_patterns(self, class_code: str, patterns: List[str]) -> None:
        """
        Add custom patterns for an equipment class at runtime
        """
        if class_code in self.patterns:
            self.patterns[class_code].extend(patterns)
        else:
            self.patterns[class_code] = patterns
        
        print(f"✅ Added {len(patterns)} custom patterns for {class_code}")