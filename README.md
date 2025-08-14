# Singapore Employment & Salary Analysis

An end-to-end data analysis project investigating how degree specialisation, industry, gender, and market competitiveness influence employment outcomes and salaries in Singapore. Uses multi-source datasets, extensive preprocessing, and visualisation to uncover trends and insights.

---

## Overview
The project addresses the question:

**"How do factors such as degree specialisation, industry, gender, and competitiveness affect employment outcomes and salary in Singapore?"**

---

## Tech Stack
- **Python**
- **pandas**, **NumPy** – Data wrangling and numerical analysis
- **matplotlib**, **seaborn** – Visualisation
- **scikit-learn** – Machine learning (Random Forest Regressor for salary prediction)

---

## Features
- Merged and cleaned multiple datasets (DF1–DF7)
- Handled missing data with imputation techniques (median, interpolation, etc.)
- Removed duplicates and addressed anomalies
- Outlier removal via **IQR** and **Z-score**
- Encoded categorical data (Ordinal Encoding)
- Applied vectorisation and clustering for school and degree grouping
- Feature engineering for enhanced insights
- Data visualisation for trends and comparisons

---

## Key Visualisations
- Labour force & population over time
- Salary vs. employment rate by degree
- Labour force by gender & qualifications
- Salary trends across industries
- Salary & employment rate by university and field
- Median salary by gender

---

## Key Insights
- Different universities yield varying average salaries and employment rates, even for the same field
- Prestigious universities (e.g., NUS Law) achieve higher outcomes due to stronger reputations
- Salaries have generally increased over time across industries
- Finance and technology are the highest paying industries
- Male–female wage differences are small in Singapore
- Influx of foreign workers increases both salaries and job market competition
- More men and women are attaining advanced degrees, boosting competitiveness
