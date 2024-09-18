import torch
from SECRET_KEYS.secret import HUGGING_FACE_TOKEN
from huggingface_hub import login
from transformers import pipeline
from data.dataframe import create_question_dataframe
import re

login(token=HUGGING_FACE_TOKEN, add_to_git_credential=True)
global NQUESTIONS
NQUESTIONS = 1
# currently #1 LLM on the leaderboard - https://huggingface.co/dnhkng/RYS-XLarge
global MODEL
MODEL = "instruction-pretrain/InstructLM-500M"
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
    
    question = {
        "question": """
        A 34 -year-old man comes to the office because of a 1 -month history of diarrhea. He has a history of pheochromocytoma 
treated 2  years ago. His mother is being treated for a tumor of her parathyroid gland. He has no other history of major 
medical illness and takes no medications. His temperature is 37.0°C  (98.6°F), pulse is 84/min, respirations are 10/min,  
and blood pressure is 120/75  mm Hg. Pulse oximetry on room air shows an oxygen saturation of 97%. Vital signs are 
within normal limits. Physical examination shows a 3 -cm, palpable mass on the right side of the neck. A biopsy specimen 
of the mass shows a n euroendocrine neoplasm of parafollicular cell origin. The most likely cause of the findings in this 
patient is a mutation in which of the following types of genes? 
        """,
        "labels": ["Cell cycle regulation gene", "DNA mismatch repair gene", "Metastasis suppressor gene", "Proto -oncogene", "Tumor suppressor gene"]
    }
    
    # iterate through each question
    for out in pipe(question["question"], candidate_labels=question["labels"]):
        llm_df.append([out["scores"]])
    
    print(llm_df)
    
"""
Parameters: pass in dataframe
Function: iterates through each row in dataframe and produces a text as well as classifiers/labels, which are yielded
"""
# def retrieve_questions(dataframe):
#     global NQUESTIONS
    
#     for i in range(NQUESTIONS):
#         print(f"{i + 1} out of {NQUESTIONS} retreived")
#         yield dataframe.iloc[i].loc["question"]

# def retrieve_choices(dataframe):
#     global NQUESTIONS
    
#     for i in range(NQUESTIONS):
#         yield find_labels(dataframe.iloc[i].loc["choices"])

# def find_labels(text: str):
#     labels = re.split("\([A-Z]\) ", text)
#     return labels[1:]
    
    
if __name__ == "__main__":
    main()