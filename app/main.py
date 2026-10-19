
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database.queries import execute_select
from app.analytics.insights import generate_insight

app = FastAPI(
    title="NL2SQL Business Analytics API",
    version="2.0.0",
)


class AskRequest(BaseModel):
    question: str


# Supported questions for the Online Retail II dataset.
RETAIL_QUERIES = {
    "total revenue": """
        SELECT ROUND(SUM(quantity * price), 2) AS total_revenue
        FROM retail_transactions
        WHERE quantity > 0 AND price > 0
    """,
    "top 5 products": """
        SELECT description,
               ROUND(SUM(quantity * price), 2) AS revenue
        FROM retail_transactions
        WHERE quantity > 0 AND price > 0
          AND description IS NOT NULL
        GROUP BY stockcode, description
        ORDER BY revenue DESC
        LIMIT 5
    """,
    "monthly revenue": """
        SELECT substr(invoicedate, 1, 7) AS month,
               ROUND(SUM(quantity * price), 2) AS revenue
        FROM retail_transactions
        WHERE quantity > 0 AND price > 0
        GROUP BY month
        ORDER BY month
    """,
    "sales by country": """
        SELECT country,
               ROUND(SUM(quantity * price), 2) AS revenue
        FROM retail_transactions
        WHERE quantity > 0 AND price > 0
        GROUP BY country
        ORDER BY revenue DESC
        LIMIT 10
    """,
    "top 5 countries": """
        SELECT country,
               ROUND(SUM(quantity * price), 2) AS revenue
        FROM retail_transactions
        WHERE quantity > 0 AND price > 0
        GROUP BY country
        ORDER BY revenue DESC
        LIMIT 5
    """,
    "top 5 customers": """
        SELECT customer_id,
               ROUND(SUM(quantity * price), 2) AS revenue
        FROM retail_transactions
        WHERE quantity > 0 AND price > 0
          AND customer_id IS NOT NULL
        GROUP BY customer_id
        ORDER BY revenue DESC
        LIMIT 5
    """,
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/questions")
def questions():
    return {"supported_questions": list(RETAIL_QUERIES.keys())}


@app.post("/ask")
def ask(req: AskRequest):
    try:
        question = req.question.strip().lower()

        sql = RETAIL_QUERIES.get(question)

        if sql is None:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Question not supported yet. Try: "
                    + ", ".join(RETAIL_QUERIES.keys())
                ),
            )

        result = execute_select(sql)
        return {
            "question": req.question,
            "sql": sql.strip(),
            "result": result,
            "insight": generate_insight(result),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
