import streamlit as st
import requests
import json
import time
from collections import defaultdict

st.set_page_config(page_title="SmartSDLC - AI Assistant", page_icon="💠", layout="wide")

st.markdown("""
<style>
    body, .main {
        background: linear-gradient(135deg,#232946 0%,#12122a 100%) !important;
        color: #dde1f5 !important;
        font-family: 'Poppins','Roboto','Inter',sans-serif;
    }
    h1, h2, h3 { color: #a3bffa !important; font-weight: 900; }
    .stButton>button {
        background: linear-gradient(90deg, #7fc8a9, #5e60ce);
        color: #fff !important; border-radius: 11px; border: none;
        font-size: 1rem; font-weight: 600; padding: 0.7rem 1.35rem;
    }
</style>
""", unsafe_allow_html=True)

API_BASE = "http://localhost:8000"


def call_api(endpoint, data=None, file=None):
    try:
        if file:
            files = {"file": file}
            res = requests.post(f"{API_BASE}/{endpoint}", files=files)
        else:
            headers = {"Content-Type": "application/json"}
            res = requests.post(f"{API_BASE}/{endpoint}", headers=headers, data=json.dumps(data))
        return res.json()
    except Exception as e:
        return {"error": str(e)}


st.sidebar.title("💠 SmartSDLC Tools")
option = st.sidebar.radio("Select a Feature:", [
    "📄 Requirement Upload & Classification",
    "🧠 AI Code Generator",
    "🛠️ Bug Fixer",
    "🧪 Test Case Generator",
    "📝 Code Summarizer",
    "💬 Smart Chat Assistant"
])

st.title("💠 SmartSDLC - AI-Enhanced Software Development Lifecycle")
st.caption("Powered by IBM Watsonx · Ultra Premium SDLC Dashboard")

# =============== REQUIREMENT UPLOAD (FINAL VERSION) ===============
if option == "📄 Requirement Upload & Classification":
    st.header("📄 Upload & Classify Requirements (PDF)")
    uploaded_file = st.file_uploader("📤 Upload your PDF document", type="pdf")

    if uploaded_file and st.button("🔍 Analyze"):
        with st.spinner("📊 Extracting and classifying requirements..."):
            result = call_api("upload-requirements", file=uploaded_file)

        if isinstance(result, list) and len(result) > 1:
            phase_groups = defaultdict(list)
            for req in result:
                phase = req.get("phase", "Unknown")
                phase_groups[phase].append(req)

            st.markdown("""
            <div style='background: linear-gradient(120deg, #303a52 60%, #232946 100%);
                        color: #fafaff; border-radius: 20px;
                        box-shadow: 0 8px 30px 0 rgba(50,40,90,0.18);
                        padding: 2.2rem 1.5rem; margin-bottom: 2.2rem;
                        border: 2.2px solid #46507d;'>
            """, unsafe_allow_html=True)

            st.markdown(f"## 📋 Total {len(result)} Requirements Extracted")

            # Display by phase
            for phase in ["Planning", "Requirements", "Design", "Implementation", "Testing", "Deployment",
                          "Maintenance"]:
                items = phase_groups.get(phase, [])
                if items:
                    st.markdown(f"### {phase} ({len(items)})")
                    for i, req in enumerate(items, 1):
                        st.markdown(f"""
                        <div style='background: #ffffff; color: #1a1a1a;
                                    border-left: 8px solid #00d4aa; border-radius: 14px;
                                    padding: 1rem 1.2rem; margin: 0.6rem 0;
                                    font-weight: 600; box-shadow: 0 3px 18px rgba(0,0,0,0.11);'>
                            🧩 {req.get('sentence', 'N/A')}
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("⚠️ Could not extract multiple requirements. Please try another PDF.")

# =============== OTHER FEATURES ===============
elif option == "🧠 AI Code Generator":
    st.header("🧠 Generate Code From Description")
    prompt = st.text_area("📝 Describe your functionality:", height=160)
    if st.button("🚀 Generate Code"):
        with st.spinner("🤖 Generating..."):
            response = call_api("generate-code", {"prompt": prompt})
        code_response = str(response.get("response", response))
        st.markdown(f"""
        <div style='background: #ffffff; color: #1a1a1a;
                    border-left: 8px solid #00d4aa; border-radius: 14px;
                    padding: 1.25rem; margin-top: 1rem;
                    box-shadow: 0 3px 18px rgba(0,0,0,0.15);'>
            {code_response}
        </div>
        """, unsafe_allow_html=True)

elif option == "🛠️ Bug Fixer":
    st.header("🛠️ AI Bug Fixer")
    buggy_code = st.text_area("Paste your buggy code:", height=210)
    if st.button("🩺 Fix Bugs"):
        with st.spinner("🔍 Analyzing..."):
            result = call_api("fix-bugs", {"code": buggy_code})
        fixed_response = str(result.get("response", result))
        st.markdown(f"""
        <div style='background: #ffffff; color: #1a1a1a;
                    border-left: 8px solid #00d4aa; border-radius: 14px;
                    padding: 1.25rem; margin-top: 1rem;
                    box-shadow: 0 3px 18px rgba(0,0,0,0.15);'>
            {fixed_response}
        </div>
        """, unsafe_allow_html=True)

elif option == "🧪 Test Case Generator":
    st.header("🧪 Automated Test Case Generator")
    function_code = st.text_area("📜 Paste your code block:", height=200)
    if st.button("🧬 Generate Tests"):
        with st.spinner("🧪 Generating..."):
            response = call_api("generate-tests", {"code": function_code})
        tests = str(response.get("response", response))
        st.code(tests, language="python")

elif option == "📝 Code Summarizer":
    st.header("📝 Code Summarization")
    code_input = st.text_area("Paste your code snippet:", height=200)
    if st.button("📚 Summarize"):
        with st.spinner("📖 Summarizing..."):
            result = call_api("summarize", {"code": code_input})
        summary = str(result.get("response", result))
        st.markdown(f"""
        <div style='background: #ffffff; color: #1a1a1a;
                    border-left: 8px solid #00d4aa; border-radius: 14px;
                    padding: 1.25rem;
                    box-shadow: 0 3px 18px rgba(0,0,0,0.15);'>
            {summary}
        </div>
        """, unsafe_allow_html=True)

elif option == "💬 Smart Chat Assistant":
    st.header("💬 Ask the SmartSDLC Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div style="text-align:right"><div style="background:linear-gradient(90deg,#5e60ce,#7fc8a9); color:#fff; border-radius:16px; padding:12px; display:inline-block; max-width:87%;">{msg["content"]}</div></div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div style="background:#22223b; color:#f2f2f2; border-radius:16px; border-left:7px solid #4cc9f0; padding:12px; display:inline-block; max-width:87%;">{msg["content"]}</div>',
                unsafe_allow_html=True)

    if prompt := st.chat_input("Ask your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("🤖 Thinking..."):
            result = call_api("chatbot", {"query": prompt})
            reply = str(result.get("response", "No response"))
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
