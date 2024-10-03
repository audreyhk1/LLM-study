import pandas as pd
import ast
from test_llm import retrieve_choices

global LANGUAGES
LANGUAGES = ["en", "es", "ar", "cs", "de", "id", "ko", "ja", "lv", "nl", "it"]

global NQUESTIONS
NQUESTIONS = 95

global FILENAMES
FILENAMES = ["scores/Yi-1.5-34B-Chat.csv"]

def main():
    global LANGUAGES, NQUESTIONS, FILENAMES
    
    # open data
    data = open_csv_to_df(FILENAMES[0], range(1, 12))
    
    # open answer choices
    answers_df = open_csv_to_df("data/qdf.csv", [2, 3]) # -> only want answer choices and answer key
    analysis_df = pd.DataFrame(index=range(NQUESTIONS), columns=LANGUAGES)
    
    # loop through each question
    for q in range(NQUESTIONS):
        # find the answer choice that correponds with correct answer key
        
        # loop through each translation
        for t in range(len(LANGUAGES)):
            pass
            # compare highest confidence score with with correct answer 
            # record result in dataframe

# convert csv to dataframe
def open_csv_to_df(filename, cols_used):
    return pd.read_csv(filename, index_col=False, usecols=cols_used)

# find the answer choice that corresponds with the correct answer key for the nth question 
def answer_key_to_answer_choice(df, index):
    pass

def convert_str_to_array(input):
    arr1, arr2 = input.split("&")
    return {"confidence": ast.literal_eval(arr1), "choices": ast.literal_eval(arr2)}
if __name__ == "__main__":
    main()