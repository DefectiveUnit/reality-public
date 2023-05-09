# Local imports
import creds

# Package imports
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
import pickle


def summarise_transcript(docs, verbose = False):
    prompt_template = """Write a dot point summary of the transcript delimited by ```, focusing on areas that would be of interest to a producer of a reality show:
            ```
            {text}
            ```
            """
    combine_template = """Write a summary of the text delimited by ```, highlighting areas that would be of interest to a producer of a reality show. 
    
            After this summary, include all the source text with the heading "Detailed notes"

            |||example
            Summary:
            Lisa is a professional kayaker. She thinks she will win due to her strong drive. <...>. <...>. She is excited to play

            Longer summary:
            - Thing #1
            - Thing #2
            - Thing #3
            ...
            |||


            ```source text
            {text}
            ```
            """
    map_prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    combine_prompt = PromptTemplate(template=combine_template, input_variables=["text"])
    llm = ChatOpenAI(temperature=0)
    
    chain = load_summarize_chain(llm=llm, chain_type='map_reduce', map_prompt=map_prompt, combine_prompt=combine_prompt, verbose=verbose)
    summary = chain.run(docs)
    return summary

def save_summary(summary, filename):
    with open(f"summaries/{filename}.txt", 'w') as f:
        f.write(summary)

def load_summary(filename):
    with open(f"summaries/{filename}.txt", 'r') as f:
        summary = f.read()
    return summary
