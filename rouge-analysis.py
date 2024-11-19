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
    rouge_df = pd.DataFrame(columns=[df.columns], index=range(NQUESTIONS))
    
    # loop through each question 
    for i, row in rewordings.iterrows():
        for n in range(row.size):
            rouge_1 = scorer.score(row[n], original[i])
            rouge_df.iat[i, n] = rouge_1["rouge1"]
    
    rouge_df.to_csv("rouge_analysis.csv")
    
if __name__ == "__main__":
    main()