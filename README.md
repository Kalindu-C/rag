Using output_parser in LangChain
The output_parser is responsible for processing the LLM's response — it should not be used directly with the output from a prompt alone.
If you want to combine a prompt, an LLM, and an output parser, the correct way is to chain them together:

python
Copy
Edit
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize components
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")
output_parser = StrOutputParser()

# Combine prompt → LLM → output parser
chain = prompt | llm | output_parser

# Run the chain
result = chain.invoke({"topic": "programming"})
print(result)
❌ Incorrect: Passing prompt.invoke() output directly into an output_parser (the parser expects an LLM response, not a prompt output).

Creating a Prompt Template for RAG
In Retrieval-Augmented Generation (RAG), you can guide the LLM to only use the provided context.
This helps reduce hallucinations and keeps answers grounded in real data.

python
Copy
Edit
from langchain_core.prompts import ChatPromptTemplate

template = """Answer the question based only on the following context:
{context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)
Why this matters: By instructing the model to only answer based on the context, you improve accuracy and reliability in RAG pipelines.