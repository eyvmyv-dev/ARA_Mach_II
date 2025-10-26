# Equipment Classifier Project Instructions

## Project Overview
This is a modular Python application for equipment classification using NLP techniques. It's designed to classify equipment from work order descriptions across multiple industries (airport, chemical processing, manufacturing, water/wastewater treatment) and is optimized for Claude Skill integration.

## Architecture
- **Core Module**: Main classification logic with confidence scoring
- **NLP Module**: Text preprocessing, tokenization, and pattern matching
- **Industry Modules**: Industry-specific classification rules and patterns
- **Utils Module**: Validation and utility functions

## Development Guidelines
- Maintain stateless design for Claude Skill compatibility
- Use clear input/output interfaces
- Implement comprehensive testing for each module
- Follow industry-specific pattern separation
- Ensure modular, testable components

## Key Technologies
- Python 3.11+
- spaCy for NLP processing
- pandas for data handling
- scikit-learn for ML components
- pytest for testing

## Project Status
✅ Project structure created
✅ Core modules implemented
✅ NLP processing components ready
✅ Industry-specific logic (Airport, Chemical, Manufacturing, Water)
✅ Testing and validation complete
✅ Claude Skill integration ready

## Usage Examples
- Basic: `python demo.py`
- Claude Skill: `python claude_skill_example.py`
- CLI: `equipment-classify --text "AHU 4.13 maintenance"`

## Next Steps
- Fine-tune confidence scoring
- Add more industry-specific patterns
- Implement ML model training
- Expand test coverage