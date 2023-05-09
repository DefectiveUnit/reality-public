# Local imports
import creds
from src.load_transcript import load_documents, get_embeddings, save_embeddings

docs = load_documents()
docsearch = get_embeddings(docs)
save_embeddings(docsearch)
