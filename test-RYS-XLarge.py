import torch
from secret import HUGGING_FACE_TOKEN
from huggingface_hub import login
from transformers import pipeline
from data.dataframe import create_question_dataframe
import re

login(token=HUGGING_FACE_TOKEN, add_to_git_credential=True)
global NQUESTIONS
NQUESTIONS = 1
# currently #1 LLM on the leaderboard - https://huggingface.co/dnhkng/RYS-XLarge
global MODEL
MODEL = "dnhkng/RYS-XLarge"
# LLM's data
global llm_df
llm_df = []

def main():
    global llm_df
    global MODEL
    
    # using the USMLE data
    df = create_question_dataframe()
    # creating a pipeline
    pipe = pipeline(model=MODEL, device=0)
    
    # iterate through each question
    for out in pipe(retrieve_questions(df), candidate_labels=retrieve_choices(df)):
        llm_df.append([out["scores"]])
    
    print(llm_df)
    
"""
Parameters: pass in dataframe
Function: iterates through each row in dataframe and produces a text as well as classifiers/labels, which are yielded
"""
def retrieve_questions(dataframe):
    global NQUESTIONS
    
    for i in range(NQUESTIONS):
        print(f"{i + 1} out of {NQUESTIONS} retreived")
        yield dataframe.iloc[i].loc["question"]

def retrieve_choices(dataframe):
    global NQUESTIONS
    
    for i in range(NQUESTIONS):
        yield find_labels(dataframe.iloc[i].loc["choices"])

def find_labels(text: str):
    labels = re.split("\([A-Z]\) ", text)
    return labels[1:]
    
    
if __name__ == "__main__":
    main()