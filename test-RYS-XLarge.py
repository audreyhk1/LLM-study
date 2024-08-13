import torch
from secret import HUGGING_FACE_TOKEN
from huggingface_hub import login
from transformers import pipeline
from data.dataframe import create_question_dataframe
import re

login(token=HUGGING_FACE_TOKEN, add_to_git_credential=True)

# currently #1 LLM on the leaderboard - https://huggingface.co/dnhkng/RYS-XLarge
MODEL = "dnhkng/RYS-XLarge"

def main():
    # using the USMLE data
    df = create_question_dataframe()
    choices = df.iloc[0].loc["choices"]
    print(re.split("\([A-Z]\) ", choices))
    
    # data(df)

"""
Parameters: pass in dataframe
Function: iterates through each row in dataframe and produces a text as well as classifiers/labels, which are yielded
"""
# def data(dataframe):
#     for i in range(3):
#         question = dataframe.iloc[i].loc["question"]
#         choices = dataframe.iloc[i].loc["choices"]

def find_labels(text: str):
    
    
if __name__ == "__main__":
    main()