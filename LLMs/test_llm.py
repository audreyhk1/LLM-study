from SECRET_KEYS.secret import HUGGING_FACE_TOKEN
from huggingface_hub import login
from transformers import pipeline
import re
import pandas as pd
import torch

login(token=HUGGING_FACE_TOKEN, add_to_git_credential=True)
global NQUESTIONS
NQUESTIONS = 95
global NLANGUAGES
NLANGUAGES = 11
# currently #1 LLM on the leaderboard - https://huggingface.co/dnhkng/RYS-XLarge
"""
Models:
1. Qwen/Qwen2.5-32B
2. 01-ai/Yi-1.5-34B-Chat
3. microsoft/Phi-3-medium-4k-instruct
4. nisten/franqwenstein-35b
5. tanliboy/lambda-qwen2.5-32b-dpo-test
6. jpacifico/Chocolatine-14B-Instruct-DPO-v1.2
7. TheTsar1209/qwen-carpmuscle-v0.1
"""
global MODEL
MODEL = "nisten/franqwenstein-35b"



"""
REMEMBER CHANGE 4 -> q in a_question and choices
remove print
"""

def main():
    print("Program started")
    global NQUESTIONS
    
    languages = ["en", "es", "ar", "cs", "de", "id", "ko", "ja", "lv", "nl", "it"]
    scores_df = pd.DataFrame(columns=languages)
    
    # using the USMLE data, create two dataframes from previously collected data, index is the question number
    translation_df, qdf = retrieve_df()
    
    # creating a pipeline
    pipe = pipeline("zero-shot-classification", model=MODEL, device=0)
    print("Pipeline created.")

    # iterate for each question
    for q in range(NQUESTIONS):
        temp_df = pd.DataFrame(index=[0], columns=languages)
        a_question = retrieve_translations(q, translation_df)       
        choices = retrieve_choices(q, qdf)
        try:
            choices.remove("")
        except ValueError:
            pass
        
        # iterate for each translation
        for t in range(NLANGUAGES):
            results = pipe(a_question[t], candidate_labels=choices)
            temp_df.iat[0, t] = str(results["scores"]) + "&" + str(results["labels"])
            print(f"{q + 1}/{NQUESTIONS} questions --- {t + 1}/{NLANGUAGES} translations")
        
            
        scores_df = pd.concat([scores_df, temp_df], ignore_index=True)
    
    folder, name = MODEL.split("/")
    scores_df.to_csv(f"{name}.csv")

"""
Parameters: pass in dataframe
Function: iterates through each row in dataframe and produces a text as well as classifiers/labels, which are yielded
"""
# read the csv with all translations -> store dataframe 
def retrieve_df(n_translations=11, n_qdf_columns=3):
    return pd.read_csv("data/question_translations.csv", index_col=False, usecols=range(1, n_translations + 1)), pd.read_csv("data/qdf.csv", index_col=False, usecols=range(1, n_qdf_columns + 1))
 
 

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