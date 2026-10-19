
import requests
import pandas as pd
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Retail Analytics Assistant",
    page_icon="📊",
    layout="wide",
)

# Styling
st.markdown("""
<style>
.main {
    background-color: #f6f8fc;
}
.block-container {
    padding-top: 2rem;
}
.hero {
    padding: 25px;
    border-radius: 16px;
    background: linear-gradient(120deg, #14213d, #2457a7);
    color: white;
    margin-bottom: 24px;
}
.hero h1 {
    color: white;
}
.metric-card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>📊 NL2SQL Business Analytics Assistant</h1>
    <p>Explore real retail transactions using natural-language questions.</p>
    <p><b>Dataset:</b> UCI Online Retail II · 2009–2011</p>
</div>
""", unsafe_allow_html=True)

SUGGESTIONS = [
    "total revenue",
    "top 5 products",
    "monthly revenue",
    "sales by country",
    "top 5 countries",
    "top 5 customers",
]

with st.sidebar:
    st.title("📈 Analytics")
    st.write("Ask a question about the retail transaction dataset.")
    st.divider()
    st.subheader("Try a question")
    for question in SUGGESTIONS:
        if st.button(question.title(), use_container_width=True):
            st.session_state["question"] = question

    st.divider()
    st.caption("Data source: UCI Machine Learning Repository")
    st.caption("Backend: FastAPI · Database: SQLite")

# Backend health
try:
    health = requests.get(f"{API_URL}/health", timeout=3)
    api_online = health.ok
except requests.RequestException:
    api_online = False

if api_online:
    st.success("Backend connected")
else:
    st.error(
        "Cannot connect to FastAPI. Start the backend first:\n\n"
        "uvicorn app.main:app --reload"
    )

st.subheader("Ask your business question")

question = st.text_input(
    "Enter a question",
    key="question",
    placeholder="e.g. monthly revenue",
)

ask_clicked = st.button(
    "🔎 Ask Database",
    type="primary",
    use_container_width=True,
)

if ask_clicked:
    if not question.strip():
        st.warning("Please enter a question.")
    elif not api_online:
        st.error("Start the FastAPI backend before asking a question.")
    else:
        with st.spinner("Querying the retail database..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question.strip()},
                    timeout=60,
                )

                if response.status_code != 200:
                    try:
                        detail = response.json().get(
                            "detail", response.text
                        )
                    except ValueError:
                        detail = response.text

                    st.error(f"Request failed: {detail}")

                else:
                    data = response.json()
                    result = data.get("result", {})
                    rows = result.get("rows", [])
                    columns = result.get("columns", [])

                    st.success("Query executed successfully")

                    st.subheader("💡 Business Insight")
                    st.info(data.get("insight", "Query completed."))

                    if rows:
                        df = pd.DataFrame(rows, columns=columns or None)

                        # Summary metrics
                        numeric_columns = df.select_dtypes(
                            include="number"
                        ).columns.tolist()

                        if len(df) == 1 and numeric_columns:
                            metric_columns = st.columns(
                                min(len(numeric_columns), 3)
                            )

                            for i, col in enumerate(
                                numeric_columns[:3]
                            ):
                                value = df[col].iloc[0]
                                metric_columns[i].metric(
                                    col.replace("_", " ").title(),
                                    f"{value:,.2f}"
                                    if pd.notna(value)
                                    else "N/A",
                                )

                        st.subheader("📋 Query Results")
                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True,
                        )

                        if len(df) > 1 and numeric_columns:
                            st.subheader("📊 Visualization")

                            label_columns = [
                                col for col in df.columns
                                if col not in numeric_columns
                            ]

                            if label_columns:
                                chart_col = st.selectbox(
                                    "Category",
                                    label_columns,
                                )
                                value_col = st.selectbox(
                                    "Measure",
                                    numeric_columns,
                                )

                                chart_df = df[
                                    [chart_col, value_col]
                                ].dropna().set_index(chart_col)

                                st.bar_chart(chart_df)

                        with st.expander("View generated SQL"):
                            st.code(data.get("sql", ""), language="sql")

                    else:
                        st.warning("The query returned no rows.")

            except requests.RequestException as exc:
                st.error(f"Could not reach the API: {exc}")

st.divider()
st.caption(
    "Academic project · Business Analytics · "
    "Symbiosis Artificial Intelligence Institute"
)
