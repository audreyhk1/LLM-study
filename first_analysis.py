import pandas as pd
import ast
import re
import os

global LANGUAGES
# IMPORTANT: assumes that the first is the original
LANGUAGES = ["en","es","ar","cs","de","id","ko","ja","lv","nl","it"]
global FILENAMES
FILENAMES = []
global NQUESTIONS
NQUESTIONS = 95

def main():
    global LANGUAGES, NQUESTIONS, FILENAMES
    
    # get filenames
    for name in os.listdir("language-rewordings/scores"):
        FILENAMES.append(f"language-rewordings/scores/{name}")
    
    # create a new 
    analysis_df = pd.DataFrame(index=range(NQUESTIONS))
    
    # open answer choices
    answers_df = pd.read_csv("Old/data/qdf.csv", index_col=False, usecols=[2, 3]) # -> only want answer choices and answer key
    
    multiple_choice = get_choices(answers_df)
    
    # loop through each LLM
    for n in range(len(FILENAMES)):
        temp_df = pd.read_csv(FILENAMES[n], index_col=[0])
        # add english translations to analysis_df
        eng_choices = answer_key_to_answer_choice(df=temp_df, qdf=answers_df, col_name=LANGUAGES[0], multiple_choice=multiple_choice, name=FILENAMES[n].removeprefix("scores/").removesuffix(".csv"))
        analysis_df = pd.concat([analysis_df, eng_choices], axis=1)
        
        """
        1) Iterate through all of the rewordings
        2) find number of different answers
        """
        # df holds all rewordings for 1 question
        rewording_df = pd.DataFrame(index=range(NQUESTIONS))
        
        # 1) iterate through all rewording types (fr, es, la, ...)
        for i in range(1, len(LANGUAGES)):
            # all of the answers the LLM chose
            rewording_choices = answer_key_to_answer_choice(df=temp_df, qdf=answers_df, col_name=LANGUAGES[i], multiple_choice=multiple_choice, name=LANGUAGES[i])
            rewording_df = pd.concat([rewording_df, rewording_choices], axis=1)

        # 2) find number of revised percent concordance
        analysis_df = pd.concat([analysis_df, calculate_revised_concordant(rewording_df, FILENAMES[n].removeprefix("scores/").removesuffix(".csv"))], axis=1)
        return
    # analysis_df.insert(0, "Correct Answer", answers_df["answer"])
    # analysis_df.to_csv("new-analysis.csv")
    
    # ndf = analysis_df[get_rpc_cols(analysis_df.columns)]
    # ndf.columns = ndf.columns.str.replace(" (Revised % Concordant)", "")
    # ndf.to_csv("rpc-calculations.csv")



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
            if llm_choices[0] in multiple_choice[ind][n] and llm_choices[0]:
                llm_choice_df.iloc[ind] = chr(n + 64 + 1)
                # already_chosen.append[llm_choices[0]]
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

"""
Parameters:
- dataframe: all of the answers for each columns for ONE LLM
- name: LLM's name

Return:
- a dataframe with all revised concordance for ONE LLM
"""
def calculate_revised_concordant(dataframe, name):
    print(name)
    print(dataframe)
    rc_df = pd.DataFrame(index=range(NQUESTIONS), columns=[f"{name} (Revised % Concordant)"])
    
    # loop through all questions
    for question_index in dataframe.index:
        # get frequency of answer choice (A, B...) from all columns
        frequency = dataframe.iloc[question_index].value_counts()
        print(frequency.max)
        rc_df.iloc[question_index] = frequency.max() / frequency.sum()
    
    return rc_df


def get_rpc_cols(columns):
    rpc_col = []
    
    for i in range(2, len(columns), 2):
        rpc_col.append(columns[i])
    
    return rpc_col

if __name__ == "__main__":
    main()