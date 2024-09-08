import pandas as pd


# question dataframe
def create_question_dataframe():
    qdf = pd.DataFrame(columns=["question", "choices", "answer"])
    QUESTION_TXT = "data/questions.txt"
    ANSWER_TXT = "data/answers.txt"
    # 119 questions
    NQUESTION = 95
    
    # reads questions
    for i in range(1, NQUESTION + 1):
        qdf.loc[len(qdf) + 1] = question_to_df(question_file=QUESTION_TXT, answer_file=ANSWER_TXT, current=i)
    
    return qdf

def main():
    create_question_dataframe().to_csv("qdf.csv")




























"""
read questions from question.txt
return question and choices as string to be stored into df

Problematic questions: 40, 115
Some of the questions refer to the image
"""
def question_to_df(question_file, answer_file, current: int):
    question = []
    question_txt = ""
    choice_txt = ""

    # opening question file
    with open(question_file, "r") as file:
        lines = file.readlines()
        qflag = False
        aflag = False
        
        for line in lines:
            if f"{current}. " in line[0:3] and current < 10:
                qflag = True
                aflag = False
                line = line[3:]
            elif f"{current}. " in line[0:4] and 10 <= current < 100:
                qflag = True
                aflag = False
                line = line[4:]
            elif f"{current}. " in line[0:5] and 100 <= current < 119:
                qflag = True
                aflag = False
                line = line[5:]
            elif "(A)" in line and qflag == True:
                qflag = False 
                aflag = True
            elif f"{current + 1}. " in line[0:5]:
                break     
            if qflag == True and aflag == False:
                question_txt += line.replace("\n", "")
            elif aflag == True and qflag == False:
                choice_txt += line
    
    # opening answer file
    with open(answer_file, "r") as file:
        for i, line in enumerate(file):
            if i == current - 1 and line.rstrip():
                return [question_txt.rstrip().replace("\n",""), choice_txt.rstrip().replace("\n",""), line[-3]]
   
if __name__ == "__main__":
    main()