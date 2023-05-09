import creds
from src.load_transcript import load_documents
from src.get_summary import summarise_transcript, save_summary

docs = load_documents(chunk_size=6000)
summary = summarise_transcript(docs)
save_summary(summary, "sample summary")