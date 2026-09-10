
"""
rag_chain.py
------------
Steps 2 and 3 of the pipeline: takes the user's question, searches the
vector database (built by ingest.py) for the most relevant chunks, and
has the LLM compose an answer strictly from that context (no
hallucination — if the info isn't in the PDFs, it says so explicitly).
 
*** This is the file Person 3 (Frontend/Router) should import from ***
 
Usage from outside (what Person 3 needs):
 
    from rag_chain import ask_hr_bot
 
    result = ask_hr_bot("How many annual leave days does an employee get?")
    print(result["answer"])
    print(result["sources"])
"""
 
import os
import time
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
 
VECTOR_STORE_DIR = "vector_store"
TOP_K = 4  # number of chunks retrieved from the vector database per question
 
# -------------------------------------------------------------------
# The prompt: defines the bot's persona and prevents it from making up
# answers that aren't grounded in the PDFs
# -------------------------------------------------------------------
SYSTEM_PROMPT = """You are an assistant that answers employee questions about
company policies and HR regulations, based ONLY on the documents provided to you.
 
Rules:
1. Answer only using the "Context" below. If the answer isn't in the context,
   say clearly: "This information is not available in the documents I have
   access to." Do not make anything up.
2. Answer in the same language the question was asked in (Arabic or English).
3. Keep your answer short, clear, and direct. Use bullet points if the
   answer has multiple details.
4. If the question is about numbers, salaries, or a specific employee's data,
   clarify that this isn't your area and suggest they ask that separately
   (a different part of the system handles that).
 
Context (taken from company documents):
{context}
"""
 
USER_PROMPT = "Question: {question}"
 
 
def _get_vector_store() -> FAISS:
    """Loads the FAISS index persisted on disk by ingest.py (without rebuilding it)."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return FAISS.load_local(
        VECTOR_STORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True,  # safe here: it's a local file we created ourselves
    )
 
 
def _format_docs(docs) -> str:
    """Turns the list of retrieved chunks into a single text block for the prompt."""
    parts = []
    for i, doc in enumerate(docs, start=1):
        source = os.path.basename(doc.metadata.get("source", "unknown"))
        page = doc.metadata.get("page", "?")
        parts.append(f"[chunk {i} - from file {source}, page {page}]\n{doc.page_content}")
    return "\n\n".join(parts)
 
 
# Built once when the module is imported, then reused for every question
_vector_store = None
_llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)

_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", USER_PROMPT),
])
 
 
def _get_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = _get_vector_store()
    return _vector_store
 
 
def ask_hr_bot(question: str) -> dict:
    """
    *** This is the function Person 3 will use to plug this part into
    the Router and the front-end ***
 
    Takes a text question and returns a dict with:
        - "answer": the final AI-generated answer text
        - "sources": list of PDF filenames + page numbers the answer was drawn from
 
    Example usage:
        result = ask_hr_bot("How many annual leave days do I get?")
        # result = {
        #   "answer": "Employees are entitled to 21 paid annual leave days...",
        #   "sources": [{"file": "leave_policy.pdf", "page": 2}, ...]
        # }
    """
    store = _get_store()
    retriever = store.as_retriever(search_kwargs={"k": TOP_K})
 
    retrieved_docs = retriever.invoke(question)
    context_text = _format_docs(retrieved_docs)
 
    chain = _prompt | _llm | StrOutputParser()
    answer = chain.invoke({"context": context_text, "question": question})
 
    sources = [
        {
            "file": os.path.basename(doc.metadata.get("source", "unknown")),
            "page": doc.metadata.get("page", "?"),
        }
        for doc in retrieved_docs
    ]
 
    return {"answer": answer, "sources": sources}
 
 
if __name__ == "__main__":
    # Quick manual test from the terminal (to confirm your part works
    # standalone before it's wired into the rest of the app)
    test_questions = [
        "How many annual leave days does an employee get?",
        "What is the sick leave policy?",
        "Does the company allow working from home?",
        "Who is the highest-paid employee?",  # intentionally out-of-scope, to check it doesn't hallucinate
    ]
    for i, q in enumerate(test_questions):
        print("\n" + "=" * 60)
        print("❓", q)
        result = ask_hr_bot(q)
        print("💬", result["answer"])
        print("📄 Sources:", result["sources"])
        if i < len(test_questions) - 1:
            time.sleep(15)  # stay under the free-tier rate limit (5 requests/min)