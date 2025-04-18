import pandas as pd
from langchain_ollama import OllamaLLM
llm_model  = OllamaLLM(base_url='http://192.168.200.18:11434', model="deepseek-r1:1.5b")  # Language model for answe generation
prompt = "Hi"
response = llm_model.invoke(prompt)
print(response)


from ollama import Client
client = Client(
  host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)
response = client.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response)



from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

llm_model  = OllamaLLM(base_url='http://192.168.200.18:11434', model="deepseek-r1:1.5b")  # Language model for answe generation
#llm_model  = OllamaLLM(base_url='http://127.0.0.1:11434', model="deepseek-r1:1.5b")  # Language model for answe generation

PROMPT_TEMPLATE = ""
You are an expert Question and Answer assistant. Use the provided context to answer the query in brief.

Query: {user_query} 
Context: {document_context} 
"""
user_query=""
context_text=""
prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
response_chain = prompt | llm_model
response = response_chain.invoke({"user_query": user_query, "document_context": context_text})