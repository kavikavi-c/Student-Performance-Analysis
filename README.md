# Student Performance Analysis

A Streamlit dashboard that analyzes student marks and shows a demo analytics page for VELoop-style user data.

## Features
- CSV upload with data validation (duplicates, missing values, wrong or out-of-range marks)
- Data quality report and missing value handling
- Statistics: mean, median, mode, standard deviation, performance distribution
- Interactive filters for students, subjects and grades
- Insights for weak students and weak subjects
- Grades, pass/fail analysis and charts
- Student search
- PDF and CSV report download
- VELoop Analytics page: engagement, XP progression, games, rewards, wallet and retention (simulated sample data)

## Technologies
Python, Pandas, NumPy, Streamlit, fpdf2

## Live Demo
https://kavitha-student-analysis.streamlit.app

## Sample Datasets
Download them from the app: Sample CSV, Test CSV (with errors), Sample VELoop CSV.

## Testing
- Clean CSV: all rows accepted, no warnings
- Test CSV with errors: duplicate, non-numeric value, marks above 100 and missing values are detected and cleaned
- Filters, search, weak-student limit and report downloads checked
- Invalid file (no Student column): error message shown

## Author
C.Kavitha
