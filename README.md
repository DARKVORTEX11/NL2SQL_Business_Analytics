# NL2SQL Business Analytics Assistant

Team: Ananth Teja, Krishna Reddy, Manu Kaul
Course: Business Analytics (0304210313)

## Run on Windows
1. Extract this ZIP. Open the extracted folder in VS Code.
2. In PowerShell: `py -m venv .venv`
3. Activate: ` .\.venv\Scripts\Activate.ps1`
4. Install: `python -m pip install -r requirements.txt`
5. Terminal 1: `uvicorn app.main:app --reload`
6. Terminal 2: `streamlit run frontend/streamlit_app.py`
7. Open the local Streamlit URL shown in the terminal.

No API key is required for the built-in demo questions. To enable general NL-to-SQL, set the GEMINI_API_KEY environment variable in PowerShell before starting uvicorn: `$env:GEMINI_API_KEY="YOUR_KEY"`. Never commit your API key to GitHub.

## Demo questions
- What is the total revenue?
- What is the average order value?
- How many customers are there?
- Show top 5 customers
- Show top 5 products
- Which product has the highest revenue?
- Show monthly revenue
- Show sales by category
- Show customers from Pune
- Which city has the highest revenue?
- What is the total number of orders?

Database contains 300 customers, 20 products, 20 employees, 1,500 orders and 1,500 payment records.
