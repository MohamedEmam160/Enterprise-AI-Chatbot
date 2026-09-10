# 🚀 Enterprise AI Assistant: The Multi-Agent Corporate Solution

> An intelligent, autonomous, and bilingual (English/Arabic) AI assistant designed to streamline enterprise operations. By leveraging a Multi-Agent architecture, it seamlessly routes user inquiries to either a RAG-based HR policy expert or a Text-to-SQL data analyst, eliminating operational bottlenecks and boosting productivity.

---

## 🎥 Project Demo (Action In Motion)
Experience the speed, accuracy, and voice-capabilities of our Enterprise AI Assistant.
**[👉 Watch the Full System Demo Here (Google Drive) 👈](PUT_YOUR_GOOGLE_DRIVE_LINK_HERE)**

---

## 💡 1. The Business Problem & ROI
In standard corporate environments, two major bottlenecks drain time and resources:
1. **HR Overload:** HR departments spend countless hours answering repetitive employee questions regarding policies, leaves, and compliance.
2. **Data Accessibility:** Executives and decision-makers lack instant access to structural data (e.g., active employees, departmental payrolls) without submitting formal IT requests.

**Our Solution:** The Enterprise AI Assistant serves as a 24/7 centralized hub. It instantly provides hallucination-free policy answers and real-time database queries, significantly reducing operational costs, ensuring absolute consistency, and enabling zero-dependency data access for management.

---

## 🏗️ 2. Core Architecture: The Maestro & Two Brains

Our system is built on a sophisticated Multi-Agent workflow, ensuring that the AI uses the right tool for the right job:

### 🚦 A. The Intelligent Router (The Maestro)
Before generating any response, the user's prompt is intercepted by a LangChain-powered Router. The Router classifies the intent of the question:
*   If the question requires numerical data or employee records -> Routes to the **SQL Agent**.
*   If the question asks about company rules, regulations, or policies -> Routes to the **RAG Agent**.

### 📖 B. The RAG Agent (HR Policy Expert)
*   **Vector Store:** Utilizes **FAISS** (Facebook AI Similarity Search) to index embedded official company PDFs.
*   **Mechanism:** When queried, it retrieves the top most relevant document chunks and synthesizes a direct answer using Google Gemini.
*   **Transparency:** It automatically cites the source document and page number, ensuring zero hallucination.

### 📊 C. The SQL Agent (Data Analyst)
*   **Mechanism:** Connects directly to the company's internal SQLite database (`company.db`).
*   **Process:** It reads the database schema, translates the user's natural language question into a secure and valid SQL query, executes it, and returns a structured `Pandas DataFrame`.

---

## ✨ 3. Key Technical Features

*   **🎙️ Smart Speech-to-Text (Voice Input):** Features a built-in audio recorder that captures voice queries. It includes a smart fallback mechanism that processes English natively and seamlessly switches to Arabic (`ar-EG`) if needed.
*   **🌍 Bilingual Processing:** The LLM prompts are optimized to understand and reply in the exact language the user initiated the conversation with.
*   **🧠 Session Memory:** Utilizes Streamlit's session state to maintain chat history, providing a natural, conversational UX similar to ChatGPT.
*   **🛡️ Secure Execution:** The SQL agent is strictly prompted to only perform `SELECT` statements, preventing unauthorized data modification.

---

## 🛠️ 4. Tech Stack & Dependencies
*   **Language:** Python
*   **LLM Engine:** Google Gemini (`gemini-3.6-flash`)
*   **Orchestration:** LangChain
*   **Databases:** FAISS (Vector) & SQLite3 (Relational)
*   **Frontend UI:** Streamlit
*   **Audio Processing:** SpeechRecognition

---

## 🚀 5. Local Installation & Setup

Want to run this project on your local machine? Follow these steps:

**1. Clone the repository:**
```bash
git clone [https://github.com/MohamedEmam160/Enterprise-AI-Chatbot.git](https://github.com/MohamedEmam160/Enterprise-AI-Chatbot.git)
cd Enterprise-AI-Chatbot
```

**2. Initialize Virtual Environment:**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

**3. Install Required Packages:**
```bash
pip install -r requirements.txt
```

**4. Environment Variables:**
Create a `.env` file in the root directory and securely add your Google API Key:
```env
GOOGLE_API_KEY="your_personal_api_key_here"
```

**5. Launch the System:**
```bash
streamlit run app.py
```

---

## 🔮 6. Future Work

Our vision for scaling this project includes:
1. **Agentic Collaboration:** Upgrading the router to allow agents to communicate with each other.
2. **Multimodal Support (Computer Vision):** Expanding the RAG capabilities to analyze scanned charts, tables, and organizational structures.
3. **Omnichannel Integration:** Porting the bot to Microsoft Teams and Slack for native workplace access.
4. **Analytics Dashboard:** Creating an admin view to track the most frequently asked questions, helping HR identify information gaps proactively.

---

## 👨‍💻 7. Contributors

This project was engineered and developed by our core team:
*   **Mostafa Sharara** - [@sharara-7](https://github.com/sharara-7)
*   **Mohamed Emam** - [@MohamedEmam160](https://github.com/MohamedEmam160)
*   **Mohamed Nader**
