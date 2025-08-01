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
FILES = ["Old/data/qdf.csv", "language-rewordings/get_translations/question_translations.csv"]

# currently #1 LLM on the leaderboard - https://huggingface.co/dnhkng/RYS-XLarge
"""
Models:
1. rombodawg/Rombos-LLM-V2.5-Qwen-32b
2. Sakalti/ultiima-32B
3. maldv/Qwentile2.5-32B-Instruct
4. Saxo/Linkbricks-Horizon-AI-Avengers-V4-32B
5. fblgit/TheBeagle-v2beta-32B-MGS
6. Sakalti/oxyge1-33B (STAR)
7. sometimesanotion/Lamarck-14B-v0.6
"""
global MODEL
MODEL = "deepseek-ai/deepseek-vl2-small"

def main():
    print("Program started")
    global NQUESTIONS, NCOLS, MODEL
        
    # using the USMLE data, create two dataframes from previously collected data, index is the question number
    rewording_df, qdf = retrieve_df()
    
    lit_levels = rewording_df.columns
    lit_levels = lit_levels.insert(0, "Original")
    scores_df = pd.DataFrame(columns=lit_levels)
    rewording_df.insert(0, "Original", qdf["question"])

    # creating a pipeline
    pipe = pipeline("zero-shot-classification", model=MODEL, device=0)
    print("Pipeline created.")

    # iterate for each question
    for q in range(NQUESTIONS):
        temp_df = pd.DataFrame(index=[0], columns=lit_levels)
        a_question = retrieve_translations(q, rewording_df)       
        choices = retrieve_choices(q, qdf)
    
        try:
            choices.remove("")
        except ValueError:
            pass
        
        # iterate for each translation
        for t in range(NCOLS):
            results = pipe(a_question[t].strip(), candidate_labels=clean_choices(choices))
            temp_df.iat[0, t] = str(results["scores"]) + "&" + str(results["labels"])
            print(f"{q + 1}/{NQUESTIONS} questions --- {t + 1}/{NCOLS} rewording")
        
        scores_df = pd.concat([scores_df, temp_df], ignore_index=True)
    
    scores_df.to_csv("scores.csv")

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
    global NCOLS
    translations = []
    
    for l in range(NCOLS):
        translations.append(dataframe.iat[index, l])
    
    return translations

def retrieve_choices(index: int, dataframe):
    global NQUESTIONS
    return find_labels(dataframe.iloc[index].loc["choices"])

def find_labels(text: str):
    labels = re.split("\([A-Z]\) ", text)
    return labels[1:]

def clean_choices(arr):
    for element in arr:
        arr[element] = element.strip()    
    
    return arr
if __name__ == "__main__":
    main()