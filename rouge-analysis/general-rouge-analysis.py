from rouge_score import rouge_scorer
import pandas as pd

global FILENAMES, NQUESTIONS
FILENAMES = ["chatgpt-rewordings/second-rewordings.csv", "data/qdf.csv"]
CSV_NAME = "chatgpt-rouge_analysis-f1-score"
NQUESTIONS = 0

def main():
    global FILENAMES, NQUESITONS, CSV_NAME
    # read questions csv
    qdf = pd.read_csv(FILENAMES[1], index_col=0)
    NQUESTIONS = len(qdf.index)
    
    # read rewordings csv
    rewordings = pd.read_csv(FILENAMES[0], index_col=0)
    
    # two datasets containing the phrases
    original = qdf["question"]
    
    # inialize scorer
    scorer = rouge_scorer.RougeScorer(["rouge1"], use_stemmer=True)
    
    # create df 
    rouge_df = pd.DataFrame(columns=[rewordings.columns], index=range(NQUESTIONS))
    
    # loop through each question 
    for i, row in rewordings.iterrows():
        for n in range(row.size - 1):
            rouge_1 = scorer.score(original.iloc[i], row[n])
            rouge_df.iat[i, n] = rouge_1["rouge1"].fmeasure
    
    rouge_df.to_csv(f"rouge-analysis/new-{CSV_NAME}.csv")

# remove/deal with any NaNs
def clean_df(df):
    pass

if __name__ == "__main__":
    main()