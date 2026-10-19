import os
SCHEMA="customers(customer_id, customer_name, age, city, state, customer_segment, registration_date); products(product_id, product_name, category, price, cost); employees(employee_id, employee_name, region); orders(order_id, customer_id, product_id, employee_id, order_date, quantity, discount, sales_amount); payments(payment_id, order_id, payment_method, payment_status)"
def demo_sql(question):
 q=question.lower()
 mappings=[(("total revenue",),"SELECT ROUND(SUM(sales_amount),2) AS total_revenue FROM orders"),(("average order value","average order"),"SELECT ROUND(AVG(sales_amount),2) AS average_order_value FROM orders"),(("how many customers","number of customers","customer count"),"SELECT COUNT(*) AS customer_count FROM customers"),(("top 5 customers","top five customers"),"SELECT c.customer_name, ROUND(SUM(o.sales_amount),2) AS total_spending FROM orders o JOIN customers c ON c.customer_id=o.customer_id GROUP BY c.customer_id ORDER BY total_spending DESC LIMIT 5"),(("top 5 products","top five products"),"SELECT p.product_name, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN products p ON p.product_id=o.product_id GROUP BY p.product_id ORDER BY revenue DESC LIMIT 5"),(("monthly revenue","revenue by month"),"SELECT substr(order_date,1,7) AS month, ROUND(SUM(sales_amount),2) AS revenue FROM orders GROUP BY month ORDER BY month"),(("sales by category","revenue by category"),"SELECT p.category, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN products p ON p.product_id=o.product_id GROUP BY p.category ORDER BY revenue DESC"),(("customers from pune","customers in pune"),"SELECT customer_id,customer_name,customer_segment FROM customers WHERE city='Pune'"),(("highest revenue" ,),"SELECT p.product_name, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN products p ON p.product_id=o.product_id GROUP BY p.product_id ORDER BY revenue DESC LIMIT 1"),(("total orders","number of orders","how many orders"),"SELECT COUNT(*) AS order_count FROM orders"),(("highest revenue city","city with the highest revenue"),"SELECT c.city, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN customers c ON c.customer_id=o.customer_id GROUP BY c.city ORDER BY revenue DESC LIMIT 1"),(("most popular payment","payment method"),"SELECT payment_method, COUNT(*) AS count FROM payments GROUP BY payment_method ORDER BY count DESC LIMIT 1")]
 for keys,sql in mappings:
  if any(k in q for k in keys): return sql
 raise ValueError("This question is not supported in demo mode. Set GEMINI_API_KEY for general NL-to-SQL generation, or try one of the sample questions.")
def generate_sql(question):
 key=os.getenv("GEMINI_API_KEY")
 if not key: return demo_sql(question)
 from google import genai
 client=genai.Client(api_key=key)
 prompt=f"Generate exactly one SQLite SELECT query for the user's question. Use only this schema: {SCHEMA}. Never modify data, never use multiple statements, and return SQL only. Question: {question}"
 response=client.models.generate_content(model="gemini-2.5-flash",contents=prompt)
 return response.text.strip().replace("```sql","").replace("```","").strip()
