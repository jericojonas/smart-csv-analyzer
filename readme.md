# Smart CSV Analyzer

A flexible CSV data analyzer and visualization tool with smart numeric column detection and interactive summaries, built with Streamlit.

## Features

- Automatically detects numeric columns, even if numbers are stored as strings with commas.
- Visualizes data distributions with histograms for numeric columns.
- Displays frequency counts for categorical columns.
- Provides detailed column summaries including total, max, min, average, and unique counts.
- Interactive selection of columns for visualization and summary.
- Supports CSV uploads through a simple web interface.

## Installation

Make sure you have Python 3.7+ installed. Then install the required packages:

```bash
pip install streamlit pandas matplotlib seaborn
````

## Usage
Run the Streamlit app with:
````
python -m streamlit run app.py
````
Upload your CSV file via the web interface, then select columns to visualize and analyze.

## How it works
The app reads your CSV file and tries to detect numeric columns, converting strings with commas into floats when possible.

For numeric columns, it shows histograms with count labels.

For categorical columns, it shows horizontal bar charts with frequency labels.

Provides a detailed summary for any selected column with aggregated statistics and unique values.

Allows selecting another column to view related values (similar to XLOOKUP functionality).

## Example
Upload a CSV file with mixed numeric and categorical data. Explore distributions and summary stats interactively.

## License
This project is licensed under the MIT License.


