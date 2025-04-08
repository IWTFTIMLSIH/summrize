import streamlit as st
import requests

st.set_page_config(page_title="Summrize", layout="centered")

st.title("📄 Summrize – Alberta Condo Doc Review")
st.write("Upload your condo documents (PDF or ZIP) and get a smart AI-powered summary.")

uploaded_file = st.file_uploader("📂 Upload condo document(s)", type=["pdf", "zip"])

if uploaded_file:
    st.info("📄 File uploaded: " + uploaded_file.name)
    with st.spinner("🔍 Reviewing your condo documents..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        try:
            response = requests.post("http://localhost:8000/upload/", files=files)
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Review complete!")

                st.subheader("🧾 Document Summary")
                st.text(data.get("extracted_text", "")[:1000] + "...")

            else:
                st.error("❌ Something went wrong: " + response.text)
        except Exception as e:
            st.error(f"❌ Failed to connect to backend: {e}")