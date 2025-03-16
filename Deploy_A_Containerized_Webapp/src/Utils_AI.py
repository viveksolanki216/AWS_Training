from langchain_community.document_loaders import PDFPlumberLoader, TextLoader, AzureAIDocumentIntelligenceLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import os

PROMPT_TEMPLATE = """
You are an expert Question and Answer assistant. Use the provided context to answer the query in brief.

Query: {user_query} 
Context: {document_context} 
"""

def read_document_to_text(file_path: str) -> list:
    # PDFPlumberLoader is a class that loads the PDF file and extracts the text from it
    # It returns a list of specific type of object i.e. Document, each object for a each page
    # consider each page as a Document, each page can be considered as a chunk
    if file_path.endswith(".pdf"):
        loader = PDFPlumberLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = AzureAIDocumentIntelligenceLoader(file_path)

    documents = loader.load() # docs is a list of Document objects
    text_in_pages = (doc.page_content for doc in documents) # a generator function
    text = "\n".join(text_in_pages)
    return text # docs is a list of Document objects

def invoke_llm(llm_model: OllamaLLM, user_query: str, context_text: str, prompt_tamplate: str) -> (str, str):
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    response_chain = prompt | llm_model
    response = response_chain.invoke({"user_query": user_query, "document_context": context_text})
    think_tags = ["<think>", "</think>"]
    idx = response.find("</think>")
    if idx != -1:
        think_notes = response[len(think_tags[0]):idx].strip('\n').strip()
        final_response = response[idx + len(think_tags[1]):].strip('\n').strip()
    else:
        final_response = response
    return think_notes, final_response


