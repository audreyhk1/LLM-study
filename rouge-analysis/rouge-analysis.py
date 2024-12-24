from rouge_score import rouge_scorer
import pandas as pd

global FILENAMES, NQUESTIONS
FILENAMES = ["get_translations/question_translations.csv"]
NQUESTIONS = 95

def main():
    global FILENAMES, NQUESITONS
    # read csv
    df = pd.read_csv(FILENAMES[0], index_col=0)
    
    # two datasets containing the phrases
    original = df["en"]
    rewordings = df.drop("en", axis=1)
    
    # inialize scorer
    scorer = rouge_scorer.RougeScorer(["rouge1"], use_stemmer=True)
    
    # create df 
    lans_col = df.columns
    rouge_df = pd.DataFrame(columns=[lans_col[1:]], index=range(NQUESTIONS))
    
    # loop through each question 
    for i, row in rewordings.iterrows():
        for n in range(row.size):
            rouge_1 = scorer.score(original[i], row[n])
            rouge_df.iat[i, n] = rouge_1["rouge1"].fmeasure
    
    rouge_df.to_csv("rouge-analysis/rouge_analysis-f1-score.csv")

def retrieve_precision(rouge_score):
    result = rouge_score.split("=").split(",")
    return result[1]
    
if __name__ == "__main__":
    main()