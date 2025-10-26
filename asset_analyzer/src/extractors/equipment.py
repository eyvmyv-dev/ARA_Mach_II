"""Equipment type extraction from work order descriptions."""

import re
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from .ml.classifier import EquipmentClassifierML

class EquipmentExtractor:
    """Extracts equipment types from work order descriptions using reference data from Equipment Classes.xlsx."""
    
    def __init__(self, equipment_classes_path: Optional[str] = None, industry: Optional[str] = None):
        """Initialize with path to Equipment Classes.xlsx and optional industry type."""
        self.config_dir = Path(__file__).parent / 'config'
        self.industry = industry
        
        # Load base patterns
        try:
            with open(self.config_dir / 'base_equipment.json') as f:
                self.base_patterns = json.load(f)
        except FileNotFoundError:
            print("Warning: base_equipment.json not found")
            self.base_patterns = {}
            
        # Load industry patterns
        try:
            with open(self.config_dir / 'industry_equipment.json') as f:
                self.industry_patterns = json.load(f).get(industry, {}) if industry else {}
        except FileNotFoundError:
            print("Warning: industry_equipment.json not found")
            self.industry_patterns = {}
            
        # Load class mappings
        try:
            with open(self.config_dir / 'class_mappings.json') as f:
                self.class_mappings = json.load(f)['mappings']
        except FileNotFoundError:
            print("Warning: class_mappings.json not found")
            self.class_mappings = {}
            
        # Initialize ML classifier
        self.ml_classifier = EquipmentClassifierML()
        
        # Load custom patterns from Excel if provided
        if equipment_classes_path is None:
            equipment_classes_path = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'Equipment Classes.xlsx'
        
        # Read equipment classes
        self.equipment_classes_df = pd.read_excel(equipment_classes_path)
        self.patterns = self._create_patterns()
        
    def _check_patterns(self, text: str, patterns: List[str]) -> float:
        """Check text against patterns and return confidence score."""
        if not text:
            return 0.0
            
        text = text.lower()
        confidence = 0.0
        
        for pattern in patterns:
            try:
                if re.search(fr'\b{pattern}\b', text, re.IGNORECASE):
                    confidence += 0.4
                    # Bonus for exact matches
                    if re.search(fr'^\s*{pattern}\s*$', text, re.IGNORECASE):
                        confidence += 0.2
            except re.error:
                # Skip invalid patterns
                continue
                
        # Add context confidence
        if self.industry == 'FACILITY':
            if re.search(r'(monthly|quarterly|annual|weekly)\s+pm', text, re.IGNORECASE):
                confidence += 0.1
            if re.search(r'building|facility|terminal|floor', text, re.IGNORECASE):
                confidence += 0.1
                
        return min(confidence, 1.0)
        
    def _create_patterns(self) -> Dict[str, list]:
        """Create regex patterns from equipment classes with enhanced matching."""
        patterns = {}
        
        # Common PM and maintenance terms to handle
        pm_patterns = [
            r'(?:annual|monthly|weekly|daily|quarterly|semi-annual)\s+pm',
            r'preventive\s+maintenance',
            r'inspection',
            r'service'
        ]
        
        # Build base patterns from equipment classes
        for _, row in self.equipment_classes_df.iterrows():
            equipment_class = row['Class']
            description = str(row['Description'])
            
            if pd.isna(description) or description.lower() == 'nan':
                continue
                
            if equipment_class not in patterns:
                patterns[equipment_class] = []
            
            # Add exact matches for equipment class code and description
            patterns[equipment_class].extend([
                re.compile(fr'\b{re.escape(equipment_class)}\b', re.IGNORECASE),
                re.compile(fr'\b{re.escape(description.lower())}\b', re.IGNORECASE)
            ])
            
            # Add equipment-specific patterns
            if equipment_class == 'BHS':
                patterns[equipment_class].extend([
                    # Component types
                    re.compile(r'\b(?:queue|transport|vertisorter|collector|diverter|merge|scanner|incline)\b', re.IGNORECASE),
                    re.compile(r'\b(?:belt|conveyor|xray|q-belt)\b', re.IGNORECASE),
                    # Location/equipment codes
                    re.compile(r'\bL\d+[-\s](?:[A-Z]+\d*[-\s]?)?\d+(?:[-\s](?:MCP|SD|VS|HSD|Transport|Queue|Belt))?\b', re.IGNORECASE),
                    re.compile(r'\bACH\b', re.IGNORECASE),  # Airport Cargo Handling
                    re.compile(r'\bHNLBHS[-\s]\d+', re.IGNORECASE),
                    # Control systems
                    re.compile(r'\b(?:motor\s*control\s*panel|main\s*control\s*panel|mcp)\b', re.IGNORECASE),
                    # General terms
                    re.compile(r'\bbaggage\b', re.IGNORECASE),
                    re.compile(r'\bsecurity\s*door\b', re.IGNORECASE),  # BHS security doors
                    # Technical components
                    re.compile(r'\b(?:gearbox|power\s*turn|tracking|tie\s*rod)\b', re.IGNORECASE)
                ])
            
            elif equipment_class == 'PBB':
                patterns[equipment_class].extend([
                    re.compile(r'\bpbb\s*\d+\b', re.IGNORECASE),
                    re.compile(r'\bgate\s*[-\s]?\s*[a-z]\d+[a-z]?\b', re.IGNORECASE),
                    re.compile(r'\bjet\s*bridge\b', re.IGNORECASE),
                    re.compile(r'\bboarding\s*bridge\b', re.IGNORECASE)
                ])
            
            elif equipment_class == 'GPU':
                patterns[equipment_class].extend([
                    re.compile(r'\bgpu\b', re.IGNORECASE),
                    re.compile(r'\bground\s*power\b', re.IGNORECASE),
                    re.compile(fr'\bgpu\s*gate\s*[-\s]?\s*[a-z]\d+[a-z]?\b', re.IGNORECASE)
                ])
            
            elif equipment_class == 'PCA':
                patterns[equipment_class].extend([
                    re.compile(r'\bpca\b', re.IGNORECASE),
                    re.compile(r'\bpre[-\s]?condition(?:ed|ing)?\s*air\b', re.IGNORECASE),
                    re.compile(fr'\bpca\s*gate\s*[-\s]?\s*[a-z]\d+[a-z]?\b', re.IGNORECASE)
                ])
            
            # Add patterns for PM work orders
            for pm_pattern in pm_patterns:
                patterns[equipment_class].append(
                    re.compile(fr'{equipment_class}\s+{pm_pattern}', re.IGNORECASE)
                )
                desc_words = description.lower().split()
                if len(desc_words) > 1:
                    patterns[equipment_class].append(
                        re.compile(fr'{desc_words[0]}\s+{pm_pattern}', re.IGNORECASE)
                    )
        
        return patterns
    
    def extract_type(self, description: str, obj_desc: Optional[str] = None) -> str:
        """Extract equipment type using hierarchical pattern matching and ML."""
        description = str(description) if description else ''
        obj_desc = str(obj_desc) if obj_desc else ''
        
        if description.lower() in ['nan', 'none', ''] and obj_desc.lower() in ['nan', 'none', '']:
            return 'Unknown'
            
        text = f"{description} {obj_desc}".lower()
        
        # Map standard categories first
        obj_class = None
        if hasattr(self, 'row_context') and 'OBJ_CLASS' in self.row_context:
            obj_class = self.row_context['OBJ_CLASS']
            
        if obj_class in self.class_mappings:
            mapping = self.class_mappings[obj_class]
            # Check patterns for the class
            for target_class, patterns in mapping['patterns'].items():
                for pattern in patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        return target_class
            # Return default mapping if no patterns match
            return mapping['default']
            
        matches = []
        
        # Get ML prediction if available
        try:
            ml_category, ml_confidence = self.ml_classifier.predict(text)
            if ml_category and ml_confidence > 0.8:
                matches.append((ml_category, 'ML_PREDICTED', ml_confidence))
        except Exception as e:
            # ML model not trained yet, skip prediction
            pass
        
        # Check industry-specific patterns first
        if self.industry and self.industry_patterns:
            for category, info in self.industry_patterns.items():
                main_conf = self._check_patterns(text, info['patterns'])
                if main_conf > 0:
                    # Check subtypes
                    max_subtype = None
                    max_subtype_conf = 0
                    for subtype, patterns in info['subtypes'].items():
                        sub_conf = self._check_patterns(text, patterns)
                        if sub_conf > max_subtype_conf:
                            max_subtype = subtype
                            max_subtype_conf = sub_conf
                    
                    final_conf = (main_conf + max_subtype_conf) / 2 if max_subtype else main_conf
                    matches.append((category, max_subtype or category, final_conf))
        
        # Check base equipment patterns
        for category, info in self.base_patterns.items():
            main_conf = self._check_patterns(text, info['patterns'])
            if main_conf > 0:
                max_subtype = None
                max_subtype_conf = 0
                for subtype, patterns in info['subtypes'].items():
                    sub_conf = self._check_patterns(text, patterns)
                    if sub_conf > max_subtype_conf:
                        max_subtype = subtype
                        max_subtype_conf = sub_conf
                
                final_conf = (main_conf + max_subtype_conf) / 2 if max_subtype else main_conf
                matches.append((category, max_subtype or category, final_conf))
        
        # Check traditional patterns as fallback
        if not matches:
            for equipment_class, pattern_list in self.patterns.items():
                confidence = 0.0
                for pattern in pattern_list:
                    if pattern.search(text):
                        confidence = max(confidence, 0.6)
                        break
                if confidence > 0:
                    matches.append((equipment_class, equipment_class, confidence))
        
        if not matches:
            return 'Other'
        
        # Check class mappings for standard categories
        if 'OBJ_CLASS' in text and text['OBJ_CLASS'] in self.class_mappings:
            obj_class = text['OBJ_CLASS']
            text_to_check = f"{text['description']} {text['obj_desc']}"
            
            # Check patterns for the class
            for target_class, patterns in self.class_mappings[obj_class]['patterns'].items():
                for pattern in patterns:
                    if re.search(pattern, text_to_check, re.IGNORECASE):
                        return target_class
                        
            # Return default mapping if no patterns match
            return self.class_mappings[obj_class]['default']
        
        # Return highest confidence match from general classification
        matches.sort(key=lambda x: x[2], reverse=True)
        return matches[0][0]  # Return main category
    
    def extract_batch(self, df, desc_col: str = 'EVT_DESC', obj_desc_col: Optional[str] = 'OBJ_DESC') -> list:
        """Extract equipment types for a batch of work orders."""
        results = []
        training_data = []
        
        for _, row in df.iterrows():
            # Set row context for classification
            self.row_context = row.to_dict() if hasattr(row, 'to_dict') else dict(row)
            
            # Extract type for current row
            equipment_type = self.extract_type(
                str(row[desc_col]),
                str(row[obj_desc_col]) if obj_desc_col in df.columns else None
            )
            results.append(equipment_type)
            
            # Collect training data if OBJ_CLASS is available and valid
            if 'OBJ_CLASS' in df.columns and pd.notna(row['OBJ_CLASS']):
                text = f"{row[desc_col]} {row[obj_desc_col]}" if obj_desc_col in df.columns else str(row[desc_col])
                training_data.append({
                    'text': text,
                    'label': row['OBJ_CLASS']
                })
        
        # Clear row context
        self.row_context = None
        
        # Update ML model with new training data if available
        if training_data:
            try:
                texts = [item['text'] for item in training_data]
                labels = [item['label'] for item in training_data]
                self.ml_classifier.update(texts, labels)
            except Exception as e:
                print(f"Warning: Could not update ML model: {str(e)}")
        
        return results