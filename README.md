# Public Health Data Insights Dashboard

A Python-based data analysis tool for researchers working with public health datasets (World Bank WDI format).

**Module**: Programming for Artificial Intelligence (WM9QF-15)
**Task**: Individual Assignment - Task 1

---

## Overview

This tool provides a complete data pipeline for public health analysis:

1. **Data Loading**: Import CSV files (World Bank WDI format)
2. **Data Cleaning**: Handle missing values, normalize schemas
3. **Data Storage**: SQLite database with normalized schema (3NF)
4. **Filtering**: Query by country code and date range
5. **Analysis**: Summary statistics, trends over time, grouped aggregations
6. **Visualization**: CLI interface with tables and matplotlib charts

**Scope**: Pre-processing and exploratory data analysis (not predictive modeling)

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

```bash
# Navigate to project directory
cd Individual-Assignment-Task-1-for-PAI

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
python main.py
```

### Run Tests

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run specific test module
python -m unittest tests.test_csv_source
```

---

## Usage Guide

When you run `python main.py`, you'll see:

```
============================================================
Public Health Data Insights Dashboard
============================================================

Menu:
1. Import data from CSV
2. Filter data
3. View summary statistics
4. Visualise trend
5. Exit

Choose option:
```

### Step-by-Step Workflow

#### 1. Import Data
- Choose option **1**
- Press **Enter** to use default path: `Plan/API_SP.DYN.LE00.IN_DS2_en_csv_v2_2505.csv`
- Wait for confirmation message

#### 2. Filter Data
- Choose option **2**
- Enter country code (e.g., `ABW`, `GBR`, `USA`) or press Enter to skip
- Enter start date in `YYYY-MM-DD` format (e.g., `2020-01-01`) or press Enter to skip
- Enter end date in `YYYY-MM-DD` format (e.g., `2024-01-01`) or press Enter to skip
- ⚠️ **Important**: Enter valid dates (e.g., `2020-01-01`, not `1967-09-88`)

#### 3. View Summary Statistics
- Choose option **3**
- See mean, min, max, and count for filtered data

#### 4. Visualize Trend
- Choose option **4**
- A matplotlib line chart appears showing trend over time
- Close the chart window to return to the menu

#### 5. Exit
- Choose option **5**

---

## Project Structure

```
Individual-Assignment-Task-1-for-PAI/
├── data/
│   ├── csv_source.py          # CSV loading and validation
│   ├── cleaner.py              # Data cleaning and normalization
│   ├── repository.py           # SQLite database operations
│   └── world_bank_sample.csv   # Sample data for testing
├── analysis/
│   ├── analyzer.py             # Statistical analysis
│   └── filters.py              # Filtering criteria
├── presentation/
│   ├── cli.py                  # CLI controller
│   └── visualizer.py           # Charts and tables
├── utils/
│   └── config.py               # Configuration constants
├── tests/
│   ├── test_csv_source.py
│   ├── test_cleaner.py
│   ├── test_repository.py
│   ├── test_filters.py
│   ├── test_analyzer.py
│   └── test_visualizer.py
├── Plan/
│   ├── system_design.md
│   ├── TDD_IMPLEMENTATION_PLAN_TASK1.md
│   ├── FINAL_DESIGN_CORRECTIONS.md
│   └── API_SP.DYN.LE00.IN_DS2_en_csv_v2_2505.csv
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Key Features

### ✅ Implemented (FR1-FR12)

- CSV data loading with validation
- World Bank WDI format normalization (wide → long)
- Missing value handling
- Type conversion (dates, numeric values)
- SQLite storage with normalized schema (3NF)
- Foreign keys and indexes for performance
- Filtering by country code and date range
- Summary statistics (mean, min, max, count)
- Trend analysis over time
- Group-by aggregation
- CLI menu interface
- Table display and line/bar charts

### 📋 Designed but Not Implemented (FR13-FR15)

- CSV export of filtered data
- CRUD update operations
- Activity logging to database

*(Discussed in reflective report as future work)*

---

## Database Schema

### Tables

**countries**
- `country_code` (TEXT, PRIMARY KEY)
- `country_name` (TEXT, NOT NULL)
- `region` (TEXT, nullable)

**indicators**
- `indicator_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `indicator_code` (TEXT, UNIQUE, NOT NULL)
- `indicator_name` (TEXT, NOT NULL)
- `category` (TEXT, nullable)

**reports**
- `report_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `country_code` (TEXT, FOREIGN KEY → countries)
- `indicator_id` (INTEGER, FOREIGN KEY → indicators)
- `report_date` (TEXT, ISO format "YYYY-01-01")
- `value` (REAL, nullable for missing data)

**Index**: `idx_reports_filters` on `(country_code, indicator_id, report_date)`

---

## Design Decisions

1. **SQLite**: Simple setup, perfect for single-user prototype
2. **pandas**: Industry-standard library for data manipulation
3. **CLI-only**: Focuses on backend logic (as per brief requirements)
4. **Normalized Schema (3NF)**: Foreign keys for data integrity
5. **TDD Approach**: Test-first development with ≥60% coverage
6. **ISO Date Format**: `YYYY-01-01` for year-level data (portability and filtering)

See [Implementation Decision Log](Plan/system_design.md#16-implementation-decision-log) for detailed rationale.

---

## Module Learning Outcomes

This project demonstrates:

- **LO1 (Software Engineering/OOP)**: Layered architecture, SOLID principles, UML/ER diagrams
- **LO2 (Python Development)**: PEP8 compliance, type hints, docstrings, effective problem-solving
- **LO3 (SQL/Databases)**: Normalized schema, parameterized queries, transaction management

See [LO Mapping](Plan/system_design.md#14-module-learning-outcomes-mapping) for full details.

---

## Testing

### Test Coverage

Target: ≥ 60% line coverage for core modules:
- `data/csv_source.py`
- `data/cleaner.py`
- `data/repository.py`
- `analysis/filters.py`
- `analysis/analyzer.py`

### Test Commands

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run specific test modules
python -m unittest tests.test_csv_source
python -m unittest tests.test_cleaner
python -m unittest tests.test_repository
python -m unittest tests.test_filters
python -m unittest tests.test_analyzer
python -m unittest tests.test_visualizer
```

---

## Known Limitations

1. **Single Dataset Format**: Optimized for World Bank WDI CSV (other formats require adaptation)
2. **CLI-Only**: Not suitable for non-technical users
3. **SQLite**: Limited concurrent write support (not for production multi-user scenarios)
4. **Basic Analytics**: Only summary statistics and trends (no correlation analysis)
5. **No Date Validation**: The system does not validate date format or validity. Users must manually enter dates in `YYYY-MM-DD` format. Invalid dates (e.g., `1967-09-88`) are not rejected and may produce unexpected results.

---

## Future Work

### Extension Features (Designed but Not Implemented)
- CSV export of filtered data
- CRUD update operations
- Activity logging to database

### Architectural Enhancements
- Abstract DataSource interface for multiple data sources
- APIDataSource for live WHO/UN data APIs
- Web dashboard (Streamlit or Flask)
- Migration to PostgreSQL for production use

---

## Design Documentation

- **[System Design](Plan/system_design.md)**: Requirements analysis (FURPS+, MoSCoW), architecture, class design, ER diagram
- **[TDD Implementation Plan](Plan/TDD_IMPLEMENTATION_PLAN_TASK1.md)**: Step-by-step TDD workflow, test specifications
- **[Design Corrections](Plan/FINAL_DESIGN_CORRECTIONS.md)**: Implementation decisions and rationale

---

## Git Workflow

This project follows TDD workflow with feature branches:
- `development` - Main development branch
- `feature/*` - Feature implementations
- `fix/*` - Bug fixes

**Branching strategy**: Feature branches merged to `development` with `--no-ff` for clear history.

---

## Dependencies

```
pandas>=2.3.3
matplotlib>=3.10.8
```

*(unittest and sqlite3 are part of Python standard library)*

---

## License

This project is submitted as coursework for WM9QF-15 (Programming for Artificial Intelligence) at the University of Warwick.
