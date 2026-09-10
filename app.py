import streamlit as st
from audio_recorder_streamlit import audio_recorder
from audio_utils import transcribe_audio
from router import route_and_execute

st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
    .stChatMessage {
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 8px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("💼 Enterprise AI Assistant")
st.caption("Query HR policies (RAG) and database records (SQL) using voice or text.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "text_val" not in st.session_state:
    st.session_state.text_val = ""

if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])
        if "data" in msg and msg["data"] is not None:
            st.dataframe(msg["data"], use_container_width=True)
        if "sources" in msg and msg["sources"]:
            with st.expander("📄 Document Sources"):
                for s in msg["sources"]:
                    st.write(f"- **File:** `{s.get('file')}` | **Page:** `{s.get('page')}`")

st.divider()

with st.container():
    col_input, col_mic, col_btn = st.columns([7, 1.2, 1.5], vertical_alignment="bottom")

    with col_mic:
        recorded_audio = audio_recorder(
            text="",
            recording_color="#e74c3c",
            neutral_color="#4A90E2",
            icon_size="28px",
            pause_threshold=2.0
        )

    if recorded_audio and recorded_audio != st.session_state.last_audio:
        st.session_state.last_audio = recorded_audio
        with st.spinner("🎙️ Transcribing audio..."):
            audio_text = transcribe_audio(recorded_audio)
            if audio_text and not audio_text.startswith("Error"):
                st.session_state.text_val = audio_text
                st.rerun()
            elif audio_text and audio_text.startswith("Error"):
                st.toast(audio_text, icon="⚠️")

    with col_input:
        user_input = st.text_input(
            "Query input",
            value=st.session_state.text_val,
            placeholder="Ask about leave policies, working hours, or employee records...",
            label_visibility="collapsed"
        )

    with col_btn:
        submit_button = st.button("Send 🚀", use_container_width=True)

if submit_button and user_input.strip():
    query = user_input.strip()

    st.session_state.text_val = ""
    st.session_state.last_audio = None

    st.chat_message("user", avatar="🧑‍💻").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Processing your request..."):
            res = None
            try:
                res = route_and_execute(query)
            except Exception as e:
                err_text = str(e)
                if "429" in err_text or "ResourceExhausted" in err_text:
                    st.warning("⏳ API quota limit reached. Please wait 30–60 seconds before trying again.")
                else:
                    st.error(f"⚠️ An unexpected error occurred: {err_text}")

            if res:
                category = res.get("category")
                st.badge(f"Routed via: {category}")

                if category == "SQL":
                    sql_query = res.get("sql_query")
                    df = res.get("data")
                    err = res.get("error")

                    with st.expander("🔍 Executed SQL Query"):
                        st.code(sql_query, language="sql")

                    if err:
                        content = f"⚠️ Query execution failed: {err}"
                        st.error(content)
                        data_to_save = None
                    elif df is not None and not df.empty:
                        content = "Here are the database records:"
                        st.markdown(content)
                        st.dataframe(df, use_container_width=True)
                        data_to_save = df
                    else:
                        content = "No matching records found in the database."
                        st.info(content)
                        data_to_save = None

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": content,
                        "data": data_to_save
                    })

                else:  # RAG route
                    answer = res.get("answer")
                    sources = res.get("sources", [])
                    st.markdown(answer)

                    if sources:
                        with st.expander("📄 Document Sources"):
                            for s in sources:
                                st.write(f"- **File:** `{s.get('file')}` | **Page:** `{s.get('page')}`")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })