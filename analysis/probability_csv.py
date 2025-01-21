import pandas as pd
import csv
from collections import Counter
import os

global FILENAME
FILENAME = ["analysis/csv/new-analysis.csv", "analysis/csv/rpc-calculations.csv"]
global NQUESTIONS
NQUESTIONS = 95
global MODELS
MODELS = os.listdir("/workspaces/LLM-calibration/scores")

def main():
    # open file containing analyzed data (analysis.csv)
    data_df = pd.read_csv(FILENAME[0], index_col=[0])
    # create df storing values
    probability_csv = pd.DataFrame()

    # get total number of question with X concordance
    totals = find_total(FILENAME[1])
    
    # loop through each column (LLM's Answers (i) & LLM's percent concordance (i + 1))
    cols = data_df.columns
    for i in range(2, len(cols), 2):
        llm_probability = find_probabilities_per_llm(llm_ans=data_df[cols[i - 1]], llm_concordant=data_df[cols[i]], large_file=data_df, totals=totals).to_frame().reset_index().drop(columns=['index']).rename(columns={0: cols[i].replace(" (Revised % Concordant)", "")})

        probability_csv = pd.concat([probability_csv, llm_probability], axis=1)
    
    probability_csv.insert(0, "% Concordance", ["10%", "20%", "30%", "40%", "50%"], True)
    
    # write df to csv
    probability_csv.to_csv("analysis/probability.csv", index=False)

"""
1. loop through each question
2. for particular question, check accuracy
3. check percent concordance 
4. add to probability
"""
def find_probabilities_per_llm(llm_ans, llm_concordant, large_file, totals):
    # create dataframe to store all probabilities for the llm
    llm_probabilities = pd.DataFrame(0, columns=["Correct", "Percent"], index=range(NQUESTIONS))
    llm_probabilities.to_csv("a.csv")
    
    # loop through every question
    for i in range(NQUESTIONS):
        llm_probabilities.iat[i, 1] = int(llm_concordant.iloc[i] * 10)
        llm_probabilities.iat[i, 0] = is_answer_correct(question_num=i, ans=llm_ans.iloc[i], large_df=large_file)
    
    # finding probabilities for each column
    concordances_w_correct_q = pd.Series(0, index=range(1,6))
    
    # if question is true
    for i in range(NQUESTIONS):
        if llm_probabilities.iat[i, 0]:
            concordances_w_correct_q[llm_probabilities.iat[i, 1]] += 1
    
    # calculate probability / total
    final_probabilities = concordances_w_correct_q.div(totals).fillna(0).astype('float64')
    return final_probabilities

def is_answer_correct(question_num, ans, large_df, col = "Correct Answer"):
    if ans in large_df[col].iloc[question_num]:
        return True
    return False

def find_total(filename=FILENAME[1]):
    totals_df = pd.read_csv(filename)
    frequency = pd.Series()
    for col in totals_df.columns:
        frequency = frequency.add(totals_df[col].value_counts(), fill_value=0)
    frequency.index = (frequency.index * 10).astype(int)
    return frequency
if __name__ == "__main__":
    main()