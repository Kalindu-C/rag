from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
# from .chroma_utils import vectorstore
from .chroma_utils import vector_store
# from .chroma_utils import dense_index


output_parser = StrOutputParser()

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Use the following context to answer the user's question."
    "if you don't find context don't answer that question."),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Set up prompts and chains
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

# print("contextualize_q_system_prompt:", contextualize_q_system_prompt)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# print("contextualize_q_prompt:", contextualize_q_prompt)

# retriever = vectorstore.as_retriever(search_kwargs={"k": 2})  #  fetches the top 2 most relevant documents

retriever_2 = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 2, "score_threshold": 0.4},
)

from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

# Initialize embeddings
embedding_function = OpenAIEmbeddings()


def get_rag_chain(model="gpt-4o-mini"):
    llm = ChatOpenAI(model=model)
    history_aware_retriever = create_history_aware_retriever(llm, retriever_2, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)    
    return rag_chain