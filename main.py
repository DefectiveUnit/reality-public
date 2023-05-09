# Local imports
#import creds
from src.load_transcript import load_documents, get_embeddings, load_embeddings

# Package imports
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain


def build_qa(build=False):
    if build:
        docs = load_documents()
        docsearch = get_embeddings(docs)
    else:
        docsearch = load_embeddings()

    llm = ChatOpenAI(temperature=0)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(search_kwargs={"k": 10}))
    return(qa, docsearch)

def get_context(user_question, docsearch):
    if len(user_question) == 0:
        return ""
    context = docsearch.similarity_search(user_question, k=4)
    return context

def get_answer(user_question, qa):
    if len(user_question) == 0:
        return ""
    
    prompt = f"""
    User question: {user_question}"        
    """
    # your code to process user_question and return answer
    answer = qa.run(user_question)
    return answer

if __name__ == "__main__":
    print("")
    #user_question = "What does Jack do for fun?"
    #qa, docsearch = build_qa()
    #context = get_context(user_question, docsearch)
    #print(context[0].page_content)
    #answer = get_answer(user_question, qa)
    #print(answer)

