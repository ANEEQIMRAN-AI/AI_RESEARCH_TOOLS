# Thesis_streamlit_app.py
import streamlit as st
from nodes_workflow import create_workflow
from tools import fetch_related_articles

def main():
    st.set_page_config(page_title="Thesis Statement Generator", layout="wide")
    st.title("🎓 Thesis Statement Generator")

    with st.container():
        col1, col2 = st.columns([1, 2])

        with col1:
            st.header("Thesis Generator")
            thesis_topic = st.text_input("Thesis topic:", placeholder="ex: Impact of consuming junk food")
            main_idea = st.text_input("Main idea about topic (optional):", placeholder="ex: Junk food is bad for the body")
            reason = st.text_input("Reason supporting main idea (optional):", placeholder="ex: Junk food creates health issues")
            audience = st.text_input("Intended audience (optional):", placeholder="ex: College students")

            colA, colB = st.columns([1, 1])
            with colA:
                if st.button("Clear Inputs"):
                    st.experimental_rerun()

            with colB:
                generate = st.button("Generate")

        with col2:
            st.header("Result")
            result_placeholder = st.empty()

        if generate:
            if thesis_topic.strip() == "":
                st.warning("Please enter a thesis topic.")
            else:
                with st.spinner("Generating thesis statements..."):
                    full_topic = thesis_topic
                    if main_idea:
                        full_topic += f" - {main_idea}"
                    if reason:
                        full_topic += f" - because {reason}"
                    if audience:
                        full_topic += f" - for {audience}"

                    workflow = create_workflow()
                    result = workflow.invoke({"topic": full_topic})
                    result_text = result["thesis_list"]

                    result_placeholder.markdown(result_text)
                    st.session_state.result_text = result_text

    # Related Articles Section
    st.markdown("---")
    st.subheader("🔍 Related Articles and Papers")

    if thesis_topic.strip():
        with st.spinner("Searching for articles..."):
            try:
                articles = fetch_related_articles(thesis_topic)
                if articles:
                    st.success("Here are related articles and papers:")
                    for i, article in enumerate(articles, start=1):
                        st.markdown(f"{i}. {article}")
                else:
                    st.warning("No recent articles found. Try refining your topic.")
            except Exception as e:
                st.error(f"Error fetching articles: {str(e)}")
    else:
        st.info("Enter a topic to fetch related articles.")

if __name__ == "__main__":
    main()