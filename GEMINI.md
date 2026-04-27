# Project Overview

This project is a Streamlit web application that serves as a classroom monitoring dashboard. It analyzes and visualizes data related to class attendance, providing insights into which classes were held, which were not, and the performance of monitoring officers. The application fetches data from a remote API, processes it, and presents it in an interactive and easy-to-understand format.

## Key Technologies

- **Frontend:** Streamlit
- **Data Processing:** Pandas, DuckDB
- **Data Visualization:** Plotly
- **Report Generation:** FPDF
- **HTTP Requests:** requests

## Functionality

- **Interactive Dashboard:** The main interface is a Streamlit dashboard that allows users to filter data by academic session, semester, and week.
- **Key Performance Indicators (KPIs):** The dashboard displays key metrics such as "Total Classes Monitored," "Total Classes Held," and "Total Classes Not Held."
- **Data Visualization:** The application uses Plotly to generate various charts, including:
  - Total classes monitored by school.
  - Total classes monitored by day of the week.
  - A list of classes that did not hold.
  - Total classes monitored per officer.
  - Total classes monitored per officer by day.
- **PDF Report Generation:** Users can generate a PDF report summarizing the monitoring data for a selected period. The report includes the KPIs and charts from the dashboard.

## Project Structure

- `app.py`: The main entry point of the Streamlit application. It handles the UI, user interactions, and orchestrates the data processing and visualization.
- `requirements.txt`: A list of all the python dependencies required to run the project.
- `components/`: This directory contains modules that encapsulate different functionalities of the application.
  - `metric.py`: This module is responsible for data fetching, cleaning, and processing. It also contains the functions for generating the Plotly charts.
  - `gen_report.py`: This module contains the logic for generating the PDF reports using the FPDF library.
  - `css.py`: This module contains the CSS code for styling the application.
- `.streamlit/`: This directory contains Streamlit configuration files.
  - `config.toml`: The main configuration file for the Streamlit application.
  - `secrets.toml`: A file for storing secrets and sensitive information.

## Running the Application

To run the application, you need to have Python and the required dependencies installed.

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

## Report Generation

The application can generate a PDF report of the classroom monitoring data. This is handled by the `gen_report.py` module, which uses the FPDF library to create the report. The report includes the KPIs and charts displayed on the dashboard. The generated report is made available for download through the application's UI.
