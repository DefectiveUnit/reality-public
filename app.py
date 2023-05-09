import streamlit as st
from main import build_qa, get_answer, get_context
from src.load_transcript import load_documents
from src.get_summary import load_summary
import re

qa, docsearch = build_qa()
docs = load_documents(chunk_size=99999999)
summary_text = load_summary("sample summary")

# Set page width
st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Transcript Q&A", page_icon=":book:")

# create sidebar menu
st.sidebar.title('Transcript Q&A')
st.sidebar.text('Enter a question about the transcript to get an answer:')

# create main content area
st.title('Ask me something about the transcript')

# create three columns
col1, col2, col3 = st.columns([1, 1, 1])

# Add custom CSS style to make the content scrollable and color timecodes
st.markdown("""
<style>
    .scrollable-left {
        max-height: 600px;
        overflow-y: scroll;
    }
    .scrollable-middle {
        max-height: 800px;
        overflow-y: scroll;
    }
    .scrollable-right {
        max-height: 800px;
        overflow-y: scroll;
    }
    .timecode {
        color: blue;
    }
</style>
""", unsafe_allow_html=True)

# add widgets to columns
with col1:
    # use the same text input box to get both user_question and docsearch
    user_question = st.text_input('Question:')
    context = get_context(user_question, docsearch)
    answer = get_answer(user_question, qa)
    st.subheader('Answer')
    st.write(answer)
    st.subheader('Context')

    # Wrap the context content inside a scrollable div with 600px height
    context_html = "<div class='scrollable-left'>"
    for i, paragraph in enumerate(context):
        # Color the timecodes blue
        paragraph_content = re.sub(r'(\[\d{2}:\d{2}:\d{2}\.\d{2}\])', r'<span class="timecode">\1</span>', paragraph.page_content)
        
        context_html += f"<p><strong>Context {i+1}</strong></p>"
        context_html += f"<p>{paragraph_content}</p>"
        context_html += "<hr>"
    context_html += "</div>"
    st.markdown(context_html, unsafe_allow_html=True)

with col2:  
    # Wrap the summary_text inside a scrollable div with 800px height
    summary_html = f"<div class='scrollable-middle'>{summary_text}</div>"
    st.subheader("Overall summary of transcript")
    st.markdown(summary_html, unsafe_allow_html=True)

with col3:
    # Wrap the content inside a scrollable div with 800px height
    st.subheader('Raw Transcript')
    content = "<div class='scrollable-right'>"
    for i, paragraph in enumerate(docs[0].page_content.split('\n\n')):
        # Color the timecodes blue
        paragraph = re.sub(r'(\[\d{2}:\d{2}:\d{2}\.\d{2}\])', r'<span class="timecode">\1</span>', paragraph)
        content += f"<p>{paragraph}</p>"
    content += "</div>"
    st.markdown(content, unsafe_allow_html=True)
