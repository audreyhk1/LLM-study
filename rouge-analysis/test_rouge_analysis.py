import pytest
from rouge_score import rouge_scorer


def main(): 
    question_six = "A 50 -year-old man comes to the office for a follow -up examination. He has a 2 -month history of headache and shortness of breath with exertion. He also has hypertension treated with hydrochlorothiazide for the past 2  years. His blood pressure is 180/105  mm Hg. Ophthalmoscopic examination is most likely to show which of the following in this patient?  "

    scorer = rouge_scorer.RougeScorer(["rouge1"], use_stemmer=True)
    # score = scorer.score(question_six, "A 50-year-old man presents for a follow-up examination. He has a 2-month history of headache and shortness of breath with exertion. He also has hypertension that has been treated with hydrochlorothiazide for 2 years. His blood pressure is 180/105 mm Hg. Which of the following tests is most likely to be seen on ophthalmoscopic examination of this patient?")
    score = scorer.score(question_six, "A 50-year-old man comes to the office for a follow-up visit. He has a 2-month history of headache and shortness of breath with exertion. He also has hypertension that has been treated with hydrochlorothiazide for the past 2 years. Blood pressure is 180/105 mm Hg. Ophthalmoscopic examination is most likely to show which of the following in this patient?")
    print(f"ROUGE-1 F1 Score: {score['rouge1'].fmeasure}")
    
    # in rouge analysis
    # use a smaller csv
    # rouge-1 calculator 
    
    
    # randomly check manually
    
    # 0 to 1
    #italian is msising !!!!

if __name__ == "__main__":
    main()