import streamlit as st
from Utils_AI import *
from streamlit_pdf_viewer import pdf_viewer

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 2000px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)
PDF_STORAGE_PATH = './data/'

st.title("CorrelationAI 👩🏻‍💻")
st.markdown("### AI Chat Assistant for PDFs")

text = ""
with st.sidebar:
    option = st.selectbox(
        "Select LLM Model",
        ("deepseek-r1:1.5b", "deepseek-r1:7b", "deepseek-r1:14b", "llama3.1:8b"),
        index=0,
        help="If the answer are not correct, choose a model with more parametes i.e. 7b or 14b. It will take more time to generate the answer.",
    )

    #LANGUAGE_MODEL = OllamaLLM(base_url='http://host.docker.internal:11434', model=option)  # Language model for answe generation
    LANGUAGE_MODEL = OllamaLLM(base_url='http://192.168.200.18:11434', model=option)  # Language model for answe generation


    uploaded_doc = st.file_uploader(
        "Upload a PDF file",
        type=["pdf"],
        help="Select a PDF document for QnA",
        accept_multiple_files=False
    )
    if uploaded_doc:
        # Save file into a local dir
        with open(PDF_STORAGE_PATH + uploaded_doc.name, "wb") as f:
            f.write(uploaded_doc.getbuffer())

        # Read Text from the file
        text = read_document_to_text(PDF_STORAGE_PATH + uploaded_doc.name)
        #with st.chat_message("user"):
        #    st.write(text)
        # write success message
        st.success("✅ Document Uploaded! Ask your questions below.")
        pdf_viewer(PDF_STORAGE_PATH + uploaded_doc.name)

user_input = st.chat_input("User Question:")
if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Thinking..."):
        # Generate AI response.
        # ai_response = generate_answer(user_input, relevant_docs)
        ai_think_notes, ai_response = invoke_llm(LANGUAGE_MODEL, user_input, text, PROMPT_TEMPLATE)

    with st.chat_message("assistant", avatar="👩🏻‍💻"):
        with st.expander("See Thinking"):
            st.write(ai_think_notes)
        st.write(ai_response)


