# Equipment Classifier

A modular NLP-based system for classifying equipment from work order descriptions across multiple industries.

## Features

- **Multi-Industry Support**: Airport, Chemical Processing, Manufacturing, Water/Wastewater
- **NLP Processing**: Advanced text preprocessing and pattern recognition
- **Confidence Scoring**: Reliability metrics for each classification
- **Claude Skill Ready**: Designed for integration with Claude Skills
- **Extensible**: Easy to add new industries and equipment types

## Installation

```bash
# Clone the repository
cd equipment_classifier

# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
from equipment_classifier import EquipmentClassifier

# Initialize for airport industry
classifier = EquipmentClassifier(industry="AIRPORT")

# Classify equipment from description
result = classifier.classify("AHU 4.13 maintenance required")
print(f"Equipment: {result.equipment_type}")
print(f"Confidence: {result.confidence:.2f}")
```

## Documentation Package 📚

This project includes comprehensive documentation designed for different audiences:

- **📖 [OVERVIEW.md](OVERVIEW.md)**: High-level explanation for non-technical stakeholders
- **🔧 [HOW_IT_WORKS.md](HOW_IT_WORKS.md)**: Detailed technical walkthrough
- **💼 [APPLICATIONS.md](APPLICATIONS.md)**: Real-world use cases and business value
- **🚀 [GETTING_STARTED.md](GETTING_STARTED.md)**: Step-by-step installation and usage guide
- **📋 [DOCUMENTATION_SUMMARY.md](DOCUMENTATION_SUMMARY.md)**: Complete technical and business summary

**Start with [OVERVIEW.md](OVERVIEW.md)** if you're new to this system.

## Project Structure

```
equipment_classifier/
├── src/
│   ├── core/                # Core classification logic
│   ├── nlp/                 # NLP processing components
│   ├── industry/            # Industry-specific modules
│   └── utils/               # Utility functions
├── tests/                   # Comprehensive test suite
├── notebooks/               # Development and examples
├── data/                    # Training data and patterns
└── config/                  # Configuration files
```

## Industries Supported

- **AIRPORT**: Air handling units, baggage systems, security equipment
- **CHEMICAL**: Process equipment, reactors, pumps, safety systems
- **MANUFACTURING**: Production equipment, conveyors, assembly systems
- **WATER**: Treatment systems, pumps, filtration equipment

## Development

```bash
# Run tests
pytest

# Format code
black src/ tests/

# Type checking
mypy src/

# Run example notebook
jupyter notebook notebooks/examples.ipynb
```

## Claude Skill Integration

This classifier is designed as a stateless component that can be easily integrated into Claude Skills:

```python
# Simple classification interface
def classify_equipment(description: str, industry: str = "AIRPORT") -> dict:
    classifier = EquipmentClassifier(industry=industry)
    result = classifier.classify(description)
    return {
        "equipment_type": result.equipment_type,
        "confidence": result.confidence,
        "context": result.context
    }
```

## License

MIT License - see LICENSE file for details.
