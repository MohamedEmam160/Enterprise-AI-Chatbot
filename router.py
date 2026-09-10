from sql_agent import ask_sql_bot
from rag_chain import ask_hr_bot
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

ROUTER_PROMPT = """You are a classifier. Determine whether the user question requires querying a structured employee SQL database OR reading HR policy documents.

Reply with EXACTLY one word: 'SQL' or 'RAG'.

- Use 'SQL' for: employee records, names, departments, salaries, hire dates, job titles, IDs.
- Use 'RAG' for: company rules, leave policies, working hours, benefits, dress code, conduct.

Question: {question}
Answer:"""

_router_llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
_prompt = ChatPromptTemplate.from_template(ROUTER_PROMPT)
_router_chain = _prompt | _router_llm | StrOutputParser()

def route_and_execute(question: str) -> dict:
    decision = _router_chain.invoke({"question": question}).strip().upper()
    
    if "SQL" in decision:
        res = ask_sql_bot(question)
        return {
            "category": "SQL",
            "sql_query": res.get("sql"),
            "data": res.get("data"),
            "error": res.get("error")
        }
    else:
        res = ask_hr_bot(question)
        return {
            "category": "RAG",
            "answer": res.get("answer"),
            "sources": res.get("sources")
        }