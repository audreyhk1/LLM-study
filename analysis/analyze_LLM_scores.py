import pandas as pd
import ast
import re
import os

global LANGUAGES
LANGUAGES = ["en", "es", "ar", "cs", "de", "id", "ko", "ja", "lv", "nl", "it", "el",]
"""
LLM1 --- Phi-3-medium-4k-instruct
"""
global NQUESTIONS
NQUESTIONS = 95
global FILENAMES
FILENAMES = []

def main():
    global LANGUAGES, NQUESTIONS, FILENAMES
    
    # get filenames
    for name in os.listdir("/workspaces/LLM-calibration/scores"):
        FILENAMES.append(f"scores/{name}")
    
    # open data
    data = pd.read_csv(FILENAMES[0], index_col=False, usecols=range(1, 12))
    analysis_df = pd.DataFrame(index=range(NQUESTIONS))
    
    # open answer choices
    answers_df = pd.read_csv("data/qdf.csv", index_col=False, usecols=[2, 3]) # -> only want answer choices and answer key
    analysis_df = pd.concat([answers_df["answer"].rename("Correct Answer"), analysis_df],axis=1)
    
    multiple_choice = get_choices(answers_df)
    
    # loop through each question
    for n in range(len(FILENAMES)):
        temp_df = pd.read_csv(FILENAMES[n], index_col=False)
        
        # add english translations to analysis_df
        eng_choices = answer_key_to_answer_choice(df=temp_df, qdf=answers_df, col_name="en", multiple_choice=multiple_choice, name=FILENAMES[n].removeprefix("scores/").removesuffix(".csv"))
        analysis_df = pd.concat([analysis_df, eng_choices], axis=1)
        
        """
        1) Iterate through all of the rewordings
        2) find number of different answers
        """
        # df holds all rewordings for 1 question
        rewording_df = pd.DataFrame(index=range(NQUESTIONS))
        
        # 1) iterate through all rewordings
        for i in range(1, len(LANGUAGES)):
            rewording_choices = answer_key_to_answer_choice(df=temp_df, qdf=answers_df, col_name=LANGUAGES[i], multiple_choice=multiple_choice, name=LANGUAGES[i])
            rewording_df = pd.concat([rewording_df, rewording_choices], axis=1)
        
        # 2) find number of wrong answers
        analysis_df = pd.concat([analysis_df, calculate_revised_concordant(rewording_df, FILENAMES[n].removeprefix("scores/").removesuffix(".csv"))], axis=1)
    
    analysis_df.to_csv("analysis/analysis.csv")



# find the answer choice that corresponds with the correct answer key for the nth question 
def answer_key_to_answer_choice(df, qdf, col_name, multiple_choice, name):
    # get response (confidence + answers) for LLM
    one_translation_df = df[col_name]
    llm_choice_df = pd.DataFrame(index=range(NQUESTIONS), columns=[name])
    
    # iterate through each question 
    for ind in one_translation_df.index:
        # get LLM's outputted choices
        confidence, llm_choices = one_translation_df[ind].split("&")
        llm_choices = ast.literal_eval(llm_choices)
        
        llm_ans = ""
        for n in range(len(multiple_choice[ind])):
            # 
            if llm_choices[0] in multiple_choice[ind][n]:
                llm_choice_df.iloc[ind] = chr(n + 64 + 1)
    return llm_choice_df

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

def calculate_revised_concordant(dataframe, name):
    rc_df = pd.DataFrame(index=range(NQUESTIONS), columns=[f"{name} (Revised % Concordant)"])
    
    for question_index in dataframe.index:
        frequency = dataframe.iloc[question_index].value_counts()
        rc_df.iloc[question_index] = frequency.iloc[0] / frequency.sum()
    
    return rc_df
    
if __name__ == "__main__":
    main()