import pandas as pd
import os

global FILENAME
FILENAME = ["analysis/analysis.csv"]
global NQUESTIONS
NQUESTIONS = 95
global NMODELS
NMODELS = len(os.listdir("/workspaces/LLM-calibration/scores"))

def main():
    # open file containing analyzed data
    data_df = pd.read_csv(FILENAME[0], index_col=False)
    
    llm_percent_accuracy = get_LLM_percent_accuracy(data_df)
    question_percent_accuracy = get_question_percent_accuracy(data_df)
    print(question_percent_accuracy)
    
    
def get_LLM_percent_accuracy(df):
    global NQUESTIONS
    df_columns = df.columns
    percent_accuracy = {}

    for col in range(2, len(df_columns), 2):
        n_wrong = df.apply(lambda x: x["Correct Answer"] if str(x["Correct Answer"]) in str(x[df_columns[col]]) else False, axis=1).value_counts()[False]
        percent_accuracy[df_columns[col]] = (NQUESTIONS - n_wrong.item()) / NQUESTIONS
    
    return percent_accuracy

def get_question_percent_accuracy(df):
    global NMODELS
    percent_accuracy = []
    df_columns = df.columns
    
    for ind in df.index: 
        n_correct = 0  
        
        for col in range(2, len(df_columns), 2):
            if df.iat[ind, 1] == df.iat[ind, col]:
                n_correct += 1
        percent_accuracy.append(n_correct / NMODELS)
    return percent_accuracy

if __name__ == "__main__":
    main()