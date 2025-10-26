# Asset Analyzer

Analyze maintenance work orders across various facility types (airports, manufacturing, etc.)

## Features

- Auto-detect work order sheets in Excel files
- Extract equipment types from descriptions
- Calculate maintenance KPIs
- Generate analysis reports

## Setup

1. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Place data files in appropriate directories:

```
data/
├── raw/          # Original Excel files
├── enriched/     # Processed data
└── reports/      # Analysis outputs
```

## Usage

### Individual Analysis

```bash
python -m asset_analyzer analyze path/to/workorders.xlsx --facility-name "My Facility"
```

### Batch Processing

```bash
python -m asset_analyzer batch  # Process all files in data/raw
```

## Development

1. Install dev dependencies:

```bash
pip install -e ".[dev]"
```

2. Run tests:

```bash
pytest
```

3. Format code:

```bash
black src tests
isort src tests
```
