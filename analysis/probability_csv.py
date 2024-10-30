import pandas as pd
import csv
import os

global FILENAME
FILENAME = ["analysis/analysis.csv"]
global NQUESTIONS
NQUESTIONS = 95
global MODELS
MODELS = os.listdir("/workspaces/LLM-calibration/scores")


def main():
    # open file containing analyzed data (analysis.csv)
    data_df = pd.read_csv(FILENAME[0], index_col=False)
    
    # create df storing values
    probability_csv = pd.DataFrame()


    # loop through each column (LLM's Answers (i) & LLM's percent concordance (i + 1))
    cols = data_df.columns
    for i in range(2, len(cols), 2):
        llm_probability = find_probabilities_per_llm(llm_name=cols[i], llm_ans=data_df[cols[i]], llm_concordant=data_df[cols[i + 1]], large_file=data_df)
        print(llm_probability)
        # probability_csv = pd.concat([probability_csv, llm_probability], ignore_index=False)
 
    # write df to csv
    # probability_csv.to_csv("probability.csv")


"""
1. loop through each question
2. for particular question, check accuracy
3. check percent concordance 
4. add to probability
"""
def find_probabilities_per_llm(llm_name, llm_ans, llm_concordant, large_file):
    # create dataframe to store all probabilities for the llm
    llm_probabilities = pd.DataFrame(0, index=["Correct", "Total"], columns=range(11))
    
    # loop through every question
    for i in range(NQUESTIONS):
        ind = int(llm_concordant.iloc[i] * 10)
        
        # check if the answer is correct
        if is_answer_correct(question_num=0, ans=llm_ans.iloc[i], large_df=large_file):
            llm_probabilities.iat[0, ind] += 1
        llm_probabilities[1, ind] += 1
    return llm_probabilities[0].div(llm_probabilities[1], axis=0)

def is_answer_correct(question_num, ans, large_df, col = "Correct Answer"):
    if ans in large_df[col].iloc[question_num]:
        return True
    return False


if __name__ == "__main__":
    main()