"""
Simple equipment classifier based on description patterns.
"""

def classify_equipment(description):
    """
    Classify equipment based on the description.
    
    Args:
        description (str): Equipment description
        
    Returns:
        str: Equipment classification
    """
    if not isinstance(description, str):
        return "Unknown"
        
    description = description.upper()
    
    # HVAC Equipment
    if "AHU" in description:
        return "Air Handling Unit"
    if "CHILLER" in description:
        return "Chiller"
    if "BOILER" in description:
        return "Boiler"
        
    # Vertical Transportation
    if "ELEVATOR" in description:
        return "Elevator"
        
    # Mechanical Systems
    if "PUMP" in description:
        return "Pump"
        
    return "Other"

def extract_equipment_id(description):
    """
    Extract equipment identifier from description if present.
    
    Args:
        description (str): Equipment description
        
    Returns:
        str: Equipment ID or None if not found
    """
    if not isinstance(description, str):
        return None
        
    # Common patterns for equipment IDs
    description = description.upper()
    
    # AHU pattern (e.g., AHU 4.13)
    if "AHU" in description:
        parts = description.split()
        idx = parts.index("AHU")
        if idx + 1 < len(parts):
            return f"AHU {parts[idx + 1]}"
            
    return None