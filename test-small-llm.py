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
    global NQUESTIONS
    
    languages = ["en", "es", "ar", "cs", "de", "id", "ko", "ja", "lv", "nl", "it"]
    scores_df = pd.DataFrame(columns=languages)
    
    # using the USMLE data, create two dataframes from previously collected data, index is the question number
    translation_df, qdf = retrieve_df()
    
    # creating a pipeline
    pipe = pipeline("zero-shot-classification", model=MODEL)
    
    
    # iterate for each question
    for q in range(NQUESTIONS):
        temp_df = pd.DataFrame(index=[0], columns=languages)
        a_question = retrieve_translations(q, translation_df)
        choices = retrieve_choices(q, qdf)
        
        # iterate for each translation
        for t in range(len(languages)):
            results = pipe(a_question[t], candidate_labels=choices)
            temp_df.iat[0, t] = results["scores"]
            print(f"{q + 1}/{NQUESTIONS} questions --- {t + 1}/{len(languages)} translations")
        
            
        scores_df = pd.concat([scores_df, temp_df])

    
    # # iterate through each question
    # for a in range(len(qdf.index)):
    #     # create a temporary dataframe to store 11 responses per translation for one question
    #     temp_df = pd.DataFrame(index=[0], columns=languages)
        
    #     # loop through every translation 
    #     for out in pipe(retrieve_questions(translation_df), candidate_labels=retrieve_choices(qdf)):
    #         print(out)
    #         return
            
            # results = 
            # print(list(results))
            # temp_df.iat[b, a] = results["scores"]
 
        # print(temp_df)   
        # return 
            
        
        # concat temp_df + scores_df
        
        
    # for out in pipe(retrieve_questions(translation_df), candidate_labels=retrieve_choices(qdf)):
    #     row_scores.append(out["scores"])
    #     if len(row_scores) == 11:
    #         scores_df.iloc[len(scores_df)] = row_scores
    #     elif len(row_scores) > 11:
    #         raise Exception("Row_score exceeded 11 elements")
        
        
        
        


    
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
        translations.append(dataframe.iat[index - 1, l])
    
    return translations

def retrieve_choices(index: int, dataframe):
    global NQUESTIONS
    return find_labels(dataframe.iloc[index].loc["choices"])


def find_labels(text: str):
    labels = re.split("\([A-Z]\) ", text)
    return labels
    
    
if __name__ == "__main__":
    main()