# Paraphraser_streamlit_app.py
import streamlit as st
from nodes_workflow import create_workflow
from tools import extract_text_from_pdf, count_words

def main():
    st.set_page_config(page_title="AI Paraphraser", layout="wide")
    
    # Initialize session state
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    if "final_output" not in st.session_state:
        st.session_state.final_output = ""

    col_input, col_output = st.columns(2)

    with col_input:
        st.markdown("## AI Paraphraser")

        # File uploader
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded_file is not None:
            st.session_state.input_text = extract_text_from_pdf(uploaded_file)

        # Text input area
        input_value = st.text_area(
            "", 
            placeholder="Start typing or paste text here...", 
            height=200, 
            value=st.session_state.input_text, 
            key="text_area"
        )
        st.session_state.input_text = input_value

        st.markdown(f"**Word Count:** {count_words(st.session_state.input_text)}")

        # Action buttons
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("Clear"):
                st.session_state.input_text = ""
                st.session_state.final_output = ""
                st.rerun()
        with col_b:
            if st.button("Paraphrase"):
                if st.session_state.input_text.strip():
                    with st.spinner("Processing..."):
                        workflow = create_workflow()
                        result = workflow.invoke({"input_paragraph": st.session_state.input_text})
                        st.session_state.final_output = result["final_output"]
                        st.rerun()
                else:
                    st.warning("Please enter a paragraph to paraphrase.")

    with col_output:
        st.markdown("## Result")
        if st.session_state.final_output:
            st.text_area("", value=st.session_state.final_output, height=500, key="result_output")
            if st.button("Copy"):
                st.toast("Copied to clipboard!")

if __name__ == "__main__":
    main()