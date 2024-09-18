import torch
from SECRET_KEYS.secret import HUGGING_FACE_TOKEN
from huggingface_hub import login
from transformers import pipeline
import re
import pandas as pd

login(token=HUGGING_FACE_TOKEN, add_to_git_credential=True)
global NQUESTIONS
NQUESTIONS = 2
global NLANGUAGES
NLANGUAGES = 11
# currently #1 LLM on the leaderboard - https://huggingface.co/dnhkng/RYS-XLarge
global MODEL
MODEL = "bigscience/bloom-560m"



def main():
    languages = ["en", "es", "ar", "cs", "de", "id", "ko", "ja", "lv", "nl", "it"]
    scores_df = pd.DataFrame(columns=languages)
    row_scores = []
    
    # using the USMLE data, create two dataframes from previously collected data
    translation_df, qdf = retrieve_df()
    
    # creating a pipeline
    pipe = pipeline("zero-shot-classification", model=MODEL)
    
    # iterate through each question
    for out in pipe(retrieve_questions(translation_df), candidate_labels=retrieve_choices(qdf)):
        row_scores.append(out["scores"])
        if len(row_scores) == 11:
            scores_df.iloc[len(scores_df)] = row_scores
        elif len(row_scores) > 11:
            raise Exception("Row_score exceeded 11 elements")
        
        
        
        


    
"""
Parameters: pass in dataframe
Function: iterates through each row in dataframe and produces a text as well as classifiers/labels, which are yielded
"""
# read the csv with all translations -> store dataframe 
def retrieve_df():
    return pd.read_csv("data/question_translations.csv"), pd.read_csv("data/qdf.csv")
 

def retrieve_questions(dataframe):
    global NQUESTIONS
    global NLANGUAGES
    
    for x in range(NQUESTIONS):
        for y in range(NLANGUAGES):
            print(f"{x + 1}/{NQUESTIONS} retreived. {y + 1}/{NLANGUAGES} retrieved.")
            yield dataframe.iloc[x].iloc[y]

def retrieve_choices(dataframe):
    global NQUESTIONS
    
    for i in range(NQUESTIONS):
        yield find_labels(dataframe.iloc[i].loc["choices"])

def find_labels(text: str):
    labels = re.split("\([A-Z]\) ", text)
    return labels[1:]
    
    
if __name__ == "__main__":
    main()