import pandas as pd
import ast
import re

global LANGUAGES
LANGUAGES = ["en", "es", "ar", "cs", "de", "id", "ko", "ja", "lv", "nl", "it"]
"""
LLM1 --- Phi-3-medium-4k-instruct
"""
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
    analysis_df = pd.DataFrame(index=range(NQUESTIONS))
    analysis_df = pd.concat([answers_df["answer"].rename("Correct Answer"), analysis_df],axis=1)
    
    multiple_choice = get_choices(answers_df)
    
    # loop through each question
    for n in range(len(FILENAMES)):
        temp_df = open_csv_to_df(FILENAMES[n], range(1, len(LANGUAGES)))
        
        # add english translations to analysis_df
        eng_choices = answer_key_to_answer_choice(df=temp_df, qdf=answers_df, col_name="en", multiple_choice=multiple_choice)
        analysis_df = pd.concat([analysis_df, eng_choices.rename(columns={"Answer choice": "Phi-3-medium-4k-instruct"})], axis=1)
        
        # for q in range(NQUESTIONS):
        #     # find the answer choice that correponds with correct answer key
            
        #     # loop through each translation
        #     for t in range(len(LANGUAGES, [1])):
        #         pass
        #         # compare highest confidence score with with correct answer 
        #         # record result in dataframe

# convert csv to dataframe
def open_csv_to_df(filename, cols_used):
    return pd.read_csv(filename, index_col=False, usecols=cols_used)


# find the answer choice that corresponds with the correct answer key for the nth question 
def answer_key_to_answer_choice(df, qdf, col_name, multiple_choice):
    # get responses for one col from df
    one_translation_df = df[col_name]
    llm_choice_df = pd.DataFrame(index=range(NQUESTIONS), columns=["Answer choice"])
    
    for ind in one_translation_df.index:
        confidence, llm_choices = one_translation_df[ind].split("&")
        llm_choices = ast.literal_eval(llm_choices)
        
        llm_ans = ""
        for n in range(len(multiple_choice[ind])):
            
            if llm_choices[0] in multiple_choice[ind][n]:
                llm_choice_df.iloc[ind] = chr(n + 64 + 1)
    return llm_choice_df
        
        

def convert_str_to_array(input):
    arr1, arr2 = input.split("&")
    return {"confidence": ast.literal_eval(arr1), "choices": ast.literal_eval(arr2)}

def get_choices(qdf):
    all_choices = []
    index = 0
    
    
    for c in qdf["choices"]:
        multiple_choice = re.split(r"\([A-Z]\) ", c)
        multiple_choice = multiple_choice[1:]
        
        # choices.append(multiple_choice[ord(answer)- 64 - 1])
        all_choices.append(multiple_choice)
        index += 1
    
    return all_choices

if __name__ == "__main__":
    main()