import streamlit as st
import PyPDF2
import io
from summarizer import summarize, extract_action_items

st.title("Meeting Transcript Summarizer")
st.caption("Paste a transcript or upload a file to get a summary and action items.")

transcript = ""

uploaded = st.file_uploader("Upload a transcript (.txt or .pdf)", type=["txt", "pdf"])

if uploaded:
    if uploaded.type == "application/pdf":
        reader = PyPDF2.PdfReader(io.BytesIO(uploaded.read()))
        transcript = " ".join(page.extract_text() for page in reader.pages)
    else:
        transcript = uploaded.read().decode("utf-8")

transcript = st.text_area("Or paste your transcript here", value=transcript, height=250)

if st.button("Summarize", type="primary"):
    if transcript.strip():
        with st.spinner("Loading model, this may take a minute on first run..."):
            summary = summarize(transcript)
            actions = extract_action_items(transcript)

        st.subheader("Summary")
        st.write(summary)

        st.subheader("Action Items")
        if actions:
            for item in actions:
                st.markdown(f"- {item}")
        else:
            st.info("No clear action items detected.")
    else:
        st.warning("Please paste a transcript first.")