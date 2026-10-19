def generate_insight(result):
 rows=result.get("rows",[])
 if not rows: return "No matching records were found."
 if len(rows)==1:
  r=rows[0]
  if len(r)==1:
   k,v=next(iter(r.items())); return f"The result for {k.replace('_',' ')} is {v}."
  first=list(r.items()); return "Top result: "+", ".join(f"{k.replace('_',' ')}: {v}" for k,v in first)+"."
 return f"The query returned {len(rows)} rows. Review the results for the business details."
