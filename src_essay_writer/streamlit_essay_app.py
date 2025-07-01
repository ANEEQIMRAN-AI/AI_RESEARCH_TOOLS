# Essay_streamlit_app.py
import streamlit as st
from nodes_workflow import create_workflow, EssayState
from tools import export_to_pdf

def main():
    st.set_page_config(page_title="AI Essay Writer", layout="centered")
    st.title("📝 AI Essay Writer ")
    st.markdown("""WELCOME TO THE AI ESSAY WRITER! This tool generates high-quality, PhD-level essays on any topic you provide. It uses advanced AI to create structured, well-researched content with proper academic formatting. You can also download the essay as a PDF file.""")

    user_topic = st.text_input("Enter your Essay Topic")
    submit = st.button("Generate Essay")

    if submit and user_topic:
        with st.spinner("Generating essay. Please wait..."):
            workflow = create_workflow()
            output = workflow.invoke({"topic": user_topic})
            final_essay = output["final_output"].content

            st.subheader("📄 Final Essay")
            st.text_area("PhD-Level Essay", final_essay, height=500)

            filename = export_to_pdf(user_topic, final_essay)
            with open(filename, "rb") as f:
                st.download_button(
                    "📥 Download Essay as PDF",
                    f,
                    file_name=filename,
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()