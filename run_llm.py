from SECRET_KEYS.secret import HUGGING_FACE_TOKEN
from huggingface_hub import login
from transformers import pipeline
import re
import pandas as pd
import torch

login(token=HUGGING_FACE_TOKEN, add_to_git_credential=True)
global NQUESTIONS
NQUESTIONS = 95
# total columns for rewordings df
global NCOLS
NCOLS = 5
global FILES
FILES = ["Old/data/qdf.csv", "chatgpt-rewordings/second-rewordings.csv"]

# currently #1 LLM on the leaderboard - https://huggingface.co/dnhkng/RYS-XLarge
"""
Models:

"""
global MODEL
MODEL = "TheTsar1209/qwen-carpmuscle-v0.1"

def main():
    print("Program started")
    global NQUESTIONS, NCOLS
        
    # using the USMLE data, create two dataframes from previously collected data, index is the question number
    rewording_df, qdf = retrieve_df()
    
    lit_levels = rewording_df.columns
    scores_df = pd.DataFrame(columns=lit_levels)
    rewording_df.insert(0, "Original", qdf["question"])
    
    
    # creating a pipeline
    pipe = pipeline("zero-shot-classification", model=MODEL, device=0)
    print("Pipeline created.")

    # iterate for each question
    for q in range(2):
        temp_df = pd.DataFrame(index=[0], columns=lit_levels)
        a_question = retrieve_translations(q, rewording_df)       
        choices = retrieve_choices(q, qdf)
        try:
            choices.remove("")
        except ValueError:
            pass
        
        # iterate for each translation
        for t in range(NCOLS):
            results = pipe(a_question[t], candidate_labels=choices)
            temp_df.iat[0, t] = str(results["scores"]) + "&" + str(results["labels"])
            print(f"{q + 1}/{NQUESTIONS} questions --- {t + 1}/{NCOLS} rewording")
        
            
        scores_df = pd.concat([scores_df, temp_df], ignore_index=True)
        break
        
    # scores_df.to_csv("scores.csv")

"""
Parameters: pass in dataframe
Function: iterates through each row in dataframe and produces a text as well as classifiers/labels, which are yielded
"""
# read the csv with all translations -> store dataframe 
def retrieve_df(n_qdf_columns=3):
    global FILES, NCOLS
    return pd.read_csv(FILES[1], index_col=False, usecols=range(1, NCOLS)), pd.read_csv(FILES[0], index_col=False, usecols=range(1, n_qdf_columns + 1))
 

# function returns the 
def retrieve_translations(index: int, dataframe):
    global NLANGUAGES
    translations = []
    
    for l in range(NLANGUAGES):
        translations.append(dataframe.iat[index, l])
    
    return translations

def retrieve_choices(index: int, dataframe):
    global NQUESTIONS
    return find_labels(dataframe.iloc[index].loc["choices"])


def find_labels(text: str):
    labels = re.split("\([A-Z]\) ", text)
    return labels
    
    
if __name__ == "__main__":
    main()