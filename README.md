# HOCR to CSV Pipeline

This project provides a Python pipeline to convert HOCR files into structured CSV files.  
It extracts text positions from HOCR, organizes items into rows and columns, cleans and normalizes the table,  
and finally generates a CSV file that can be used for further processing or analysis.

## Features
- Parse HOCR files and extract text positions.
- Sort data by vertical (`y1`) and horizontal (`x1`) positions.
- Group items into rows based on vertical proximity.
- Detect column positions and align text properly.
- Clean and normalize tables before generating CSV output.
- Full pipeline available through a single function: `hocr_to_csv`.

## Jupyter Notebook
A Jupyter Notebook is included in this repository to explore and run the pipeline interactively.  
It contains:
- Step-by-step instructions to process HOCR files.
- Examples of using each function (`order_data`, `group_into_rows`, `detect_columns`, `clean_and_normalize_table`, `build_csv`, `hocr_to_csv`).
- Code snippets to install required libraries if they are not already installed.

## Requirements
Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
