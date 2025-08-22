from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
import os

from dotenv import load_dotenv
load_dotenv()

# Import the Pinecone library
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Create a dense index with integrated embedding
index_name = "quickstart-py"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Target the index
index = pc.Index(index_name)

embeddings = OpenAIEmbeddings()

vector_store = PineconeVectorStore(index=index, embedding=embeddings)
# vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)



def load_and_split_document(file_path: str) -> List[Document]:
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.html'):
        loader = UnstructuredHTMLLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
    
    documents = loader.load()
    return text_splitter.split_documents(documents)

def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    try:
        splits = load_and_split_document(file_path)
        
        # Add metadata to each split
        for split in splits:
            split.metadata['file_id'] = file_id

        # vectorstore.add_documents(splits)
        vector_store.add_documents(documents=splits)

        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False

def delete_doc_from_chroma(file_id: int):
    try:
        # Delete using metadata filter
        index.delete(
            filter={"file_id": {"$eq": file_id}}
        )
        print(f"Deleted all documents with file_id {file_id}")
        return True
    
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {str(e)}")
        return False