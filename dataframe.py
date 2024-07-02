import pandas as pd

def main():
    QUESTION_TXT = "data/questions.txt"
    ANSWER_TXT = "data/answers.txt"
    
    # reads questions
    for i in range(1, 6):
        question = question_to_df(question_file=QUESTION_TXT, answer_file=ANSWER_TXT, current=i)
        

"""
read questions from question.txt
return question and choices as string to be stored into df

Problematic questions: 40, 115
Some of the questions refer to the image
"""
def question_to_df(question_file, answer_file, current: int):
    question = {"question": "", "choices": "", "answer": ""}

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
                question["question"] += line.replace("\n", "")
            elif aflag == True and qflag == False:
                question["choices"] += line.replace("\n", ", ")
    
    # opening answer file
    with open(answer_file, "r") as file:
        for i, line in enumerate(file):
            if i == current - 1:
                question["answer"] = line[-3]
                break

    return question
    
        
    
if __name__ == "__main__":
    main()