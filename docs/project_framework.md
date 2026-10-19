# Project Framework
## Problem statement
Non-technical business users often need SQL knowledge to retrieve insights from relational databases. This project allows users to ask business questions in natural language and receive validated database-backed answers.
## Objectives
1. Convert natural language questions to SQL. 2. Execute validated read-only queries. 3. Return clear results. 4. Support business analytics such as revenue, customers, products and trends. 5. Display tables/charts.
## Methodology
Question -> schema-aware SQL generation -> validation -> SQL execution -> insight and visualization.
## Dataset
Synthetic retail/business dataset: Customers, Products, Employees, Orders, Payments.
## Stack
Python, FastAPI, SQLite, Streamlit, Pandas, optional Gemini API.
