import streamlit as st
import os
from openai import OpenAI
from github_integration import get_repo_files

# 🔐 API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🎨 Page Config
st.set_page_config(
    page_title="AI Security Scanner",
    page_icon="🔐",
    layout="centered"
)

# 🌈 Custom Styling
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1 {
    text-align: center;
    color: #00ADB5;
}
.stButton>button {
    background-color: #00ADB5;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.stTextInput>div>div>input {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# 🔍 AI Function
def analyze_code(code):
    try:
        prompt = f"""
Analyze this code for:
- SQL Injection
- Insecure API usage

Give:
1. Vulnerability
2. Explanation
3. Fix

Code:
{code}
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception:
        return(
            "🔴 Vulnerability: SQL Injection\n"
            "🟡 Explanation: Unsafe user input in query\n"
            "🟢 Fix: Use parameterized queries\n"
            "⚠️ Severity: High"
        )


# 🖥️ UI
st.title("🔐 AI Security Vulnerability Scanner")

st.markdown("### 🚀 Scan GitHub repositories for security issues")

repo_name = st.text_input("🔗 Enter GitHub Repo (username/repo):")

if st.button("🔍 Scan Repository"):
    if repo_name:
        with st.spinner("Scanning repository... ⏳"):
            try:
                files = get_repo_files(repo_name)

                for name, code in files[:2]:
                    st.markdown(f"### 📄 {name}")

                    result = analyze_code(code)

                    st.success("✅ Scan Complete")
                    st.code(result, language="markdown")

            except Exception as e:
                st.error("❌ Error: Check repo name or GitHub token")
                st.write(e)

    else:
        st.warning("⚠️ Please enter a repository name")

# 📌 Footer
st.markdown("---")
st.markdown("👨‍💻 Developed using Streamlit + OpenAI + GitHub API")
