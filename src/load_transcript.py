from langchain.document_loaders import DirectoryLoader #file loading
from langchain.text_splitter import CharacterTextSplitter #split the docs
from langchain.vectorstores import FAISS #vector store
from langchain.embeddings.openai import OpenAIEmbeddings #embeddings
from langchain import PromptTemplate, FewShotPromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from typing import List
import creds
import pickle
import datetime
import os
import glob

# Load all pptx docs - note: more efficient is to save these embedded docs to disk and load each time, rather than running the embeddings each time

def load_documents(filename: str = '**/*.docx', chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Load text documents from a directory and split them into chunks.

    Args:
        filename (str): Name or pattern to match text documents in a directory.
        chunk_size (int, optional): Number of characters in each text chunk. Default is 250.
        chunk_overlap (int, optional): Number of characters to overlap between adjacent text chunks. Default is 50.

    Returns:
        List[str]: A list of text chunks, each representing a portion of a document.

    Raises:
        FileNotFoundError: If the specified directory or file does not exist.

    Examples:
        >>> docs = load_documents('my_folder/*.txt', chunk_size=200, chunk_overlap=50)
        >>> len(docs)
        1000
        >>> docs[0][:50]
        'It was a bright cold day in April, and the clocks '
    """
    loader = DirectoryLoader('..', glob=filename)
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = loader.load_and_split(text_splitter=text_splitter)
    return docs


def get_embeddings(docs):
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_documents(docs, embeddings)
    return docsearch

# This doesn't work
def save_embeddings(docsearch, doc_name=None):
    if doc_name is None:
        # use the current date and time as the default name
        now = datetime.datetime.now()
        doc_name = now.strftime('%Y-%m-%d_%H-%M-%S')

    docsearch.save_local(f"vector_db/{doc_name}")


def load_embeddings(doc_name=None):
    if doc_name is None:
        # find the most recent pickle file in the pickles directory
        vector_dirs = glob.glob('vector_db/*')
        vector_dirs.sort(key=os.path.getmtime)
        doc_name = os.path.splitext(os.path.basename(vector_dirs[-1]))[0]

    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.load_local(f"vector_db/{doc_name}", embeddings)
    return docsearch

def add_to_db(docsearch, text):
    # To write
    """
    new_docs = [...]  # List of new documents
    vectordb.add_texts(new_docs)
    """
    return