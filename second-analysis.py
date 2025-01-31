import pandas as pd
import csv
from collections import Counter
import os

global FILENAME
FILENAME = ["language-rewordings/new-csv/new-analysis.csv", "language-rewordings/new-csv/rpc-calculations.csv"]
global NQUESTIONS
NQUESTIONS = 95
global MODELS
MODELS = os.listdir("/workspaces/LLM-calibration/scores")

# 1/(# of rewordings) --> 1/10, 1/4
global PERCENT_INTERVALS
PERCENT_INTERVALS = ["30", "40", "50", "60", "70", "80", "90", "100"]

def main():
    global PERCENT_INTERVALS
    # open file containing analyzed data (analysis.csv)
    data_df = pd.read_csv(FILENAME[0], index_col=[0])
    # create df storing values
    probability_csv = pd.DataFrame()

    # loop through each column (LLM's Answers (i) & LLM's percent concordance (i + 1))
    cols = data_df.columns
    for i in range(2, len(cols), 2):
        llm_probability = find_probabilities_per_llm(
                llm_ans=data_df[cols[i - 1]], 
                llm_concordant=data_df[cols[i]], 
                large_file=data_df, 
                totals=find_total(llm_n=cols[i-1])
            ).to_frame().reset_index().drop(columns=['index']).rename(columns={0: cols[i].replace(" (Revised % Concordant)", "")})
        probability_csv = pd.concat([probability_csv, llm_probability], axis=1)
    print("Collected Concordance!")
    probability_csv.insert(0, "% Concordance", PERCENT_INTERVALS, True)
    
    # loop through each llm
    cols = probability_csv.columns[1:]  # Exclude % Concordance

    for n_llm in cols:  # Directly iterate over column names
        totals = find_total(llm_n=n_llm)  # Get totals for this column
        
        for c in range(len(probability_csv.index)):  # Iterate over rows
            probability_csv.at[c, n_llm] = float(probability_csv.at[c, n_llm])  # Convert value
            probability_csv.at[c, n_llm] *= totals[c] / NQUESTIONS  # Apply weight
            
            
    # write df to csv
    probability_csv.to_csv("probability.csv", index=False)

"""
1. loop through each question
2. for particular question, check accuracy
3. check percent concordance 
4. add to probability
"""
def find_probabilities_per_llm(llm_ans, llm_concordant, large_file, totals):
    global PERCENT_INTERVALS
    # create dataframe to store all probabilities for the llm
    llm_probabilities = pd.DataFrame(0, columns=["Correct", "Percent"], index=range(NQUESTIONS))
    
    # loop through every question
    for i in range(NQUESTIONS):
        llm_probabilities.iat[i, 1] = llm_concordant.iloc[i] * 100
        llm_probabilities.iat[i, 0] = is_answer_correct(question_num=i, ans=llm_ans.iloc[i], large_df=large_file)
    
    # llm_probabilities now contains 2 cols: 
    # "Correct" which is whether or not the LLM got the Original rewording correct (bool)
    # "Percent": Revised Percent Concordance (10, 50, ...)

    # finding probabilities for each column (PERCENT_INTERVALS as the keys for the Series)
    concordances_w_correct_q = pd.Series(0, PERCENT_INTERVALS)
    
    # if question is true
    for i in range(NQUESTIONS):
        if llm_probabilities.iat[i, 0]:
            concordances_w_correct_q.loc[str(llm_probabilities.iat[i, 1])] += 1
    # calculate probability / total
    final_probabilities = concordances_w_correct_q.div(totals).fillna(0).astype('float64')
    return final_probabilities

def is_answer_correct(question_num, ans, large_df, col = "Correct Answer"):
    if ans in large_df[col].iloc[question_num]:
        return True
    return False

# find the total counts for each potential revised percent concordance value
def find_total(llm_n, filename=FILENAME[1]):
    global PERCENT_INTERVALS
    totals_df = pd.read_csv(filename)
    temp = totals_df[[llm_n]].value_counts().sort_index().reset_index(drop=True)
    temp.index = range(len(PERCENT_INTERVALS) - 1, len(PERCENT_INTERVALS) - len(temp) - 1, -1)
    temp.index = temp.index[::-1]
    t = pd.Series(index=range(len(PERCENT_INTERVALS)), name=llm_n)
    merged = t.combine_first(temp).reindex(index=t.index).fillna(0)
    return pd.Series(data=merged.values, index=PERCENT_INTERVALS, name=llm_n)

if __name__ == "__main__":
    main()