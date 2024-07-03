import pandas as pd

# question dataframe
global questions_df
qdf = pd.DataFrame(columns=["question", "choices", "answer"])

def main():
    global qdf
    QUESTION_TXT = "data/questions.txt"
    ANSWER_TXT = "data/answers.txt"
    
    # reads questions
    for i in range(1, 5):       
        qdf.loc[len(qdf)] = question_to_df(question_file=QUESTION_TXT, answer_file=ANSWER_TXT, current=i)
        

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
            if f"{current}. " in line[0:3]:
                qflag = True
                aflag = False
                line = line[3:]
            elif "(A)" in line and qflag == True:
                qflag = False 
                aflag = True
            elif f"{current + 1}. " in line[0:3]:
                break     
            if qflag == True and aflag == False:
                question_txt += line.replace("\n", "")
            elif aflag == True and qflag == False:
                choice_txt += line.replace("\n", ", ")
    
    # opening answer file
    with open(answer_file, "r") as file:
        for i, line in enumerate(file):
            if i == current - 1:
                return [question_txt.rstrip(), choice_txt.rstrip(), line[-3]]

    
        
    
if __name__ == "__main__":
    main()