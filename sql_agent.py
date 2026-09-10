import sqlite3
import pandas as pd
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

DB_PATH = "company.db"

def get_schema() -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    lines = []
    for t in tables:
        cur.execute(f"PRAGMA table_info({t})")
        cols = [row[1] for row in cur.fetchall()]
        lines.append(f"{t}({', '.join(cols)})")
    conn.close()
    return "\n".join(lines)

schema_text = get_schema()

SYSTEM_PROMPT = """You are a SQLite expert. Given the database schema below, write exactly ONE valid SQLite SELECT query that answers the user's question.

Schema:
{schema}

Rules:
- Output ONLY the raw SQL statement, nothing else.
- Do NOT wrap the query in markdown formatting (no ```sql or ```).
- End the statement with a semicolon (;).
- Use only tables and columns from the schema above.
- Use LOWER() or LIKE for string comparisons so filtering is case-insensitive (e.g., LOWER(status) = 'active').
"""

llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)

_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}")
])

def extract_sql(text: str) -> str:
    t = text.strip()
    if "```" in t:
        parts = t.split("```")
        if len(parts) >= 2:
            t = parts[1]
            if t.lower().startswith("sql"):
                t = t[3:]
    t = t.strip()
    if ";" in t:
        t = t.split(";")[0] + ";"
    return t.strip()

def ask_sql_bot(question: str) -> dict:
    chain = _prompt | llm | StrOutputParser()
    raw_query = chain.invoke({"schema": schema_text, "question": question})
    sql = extract_sql(raw_query)
    
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
        error = None
    except Exception as e:
        df = None
        error = str(e)
    finally:
        conn.close()
        
    return {"sql": sql, "data": df, "error": error}

if __name__ == "__main__":
    test_q = "List all active employees and their job titles"
    res = ask_sql_bot(test_q)
    print("Generated SQL:", res["sql"])
    print("Data:\n", res["data"])