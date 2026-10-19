import re
FORBIDDEN={"INSERT","UPDATE","DELETE","DROP","ALTER","TRUNCATE","CREATE","REPLACE","ATTACH","DETACH","PRAGMA"}
def validate_sql(sql):
    s=re.sub(r"--.*?$|/\*.*?\*/", "", sql, flags=re.M|re.S).strip().rstrip(";")
    if not re.match(r"(?is)^SELECT\b",s): raise ValueError("Only read-only SELECT queries are permitted.")
    if ";" in s: raise ValueError("Multiple SQL statements are not allowed.")
    for word in FORBIDDEN:
        if re.search(rf"\b{word}\b",s,re.I): raise ValueError(f"Unsafe SQL operation detected: {word}")
    return s
