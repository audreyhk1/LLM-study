import pandas as pd
from translate_libraries.final_translate import lang_translation
from openpyxl.workbook import Workbook

global LANGUAGES
LANGUAGES = ["en", "es", "ar", "cs", "de", "id", "ko", "ja", "lv", "nl", "it"] 

def main():
    global LANGUAGES
    
    qdf = pd.read_csv("data/qdf.csv")
    # selects only the questions where "questions" is a series
    questions = qdf["question"]
    
    # create a translated quetion dataframe (seperate from the qdf but linked through the index)
    translated_qdf = pd.DataFrame(columns=LANGUAGES)
    
    # for question 
    for index, value in questions.items():
        translated_qdf = translated_qdf._append(retrieve_10_translations(number=index, text=value, languages=LANGUAGES[1:]), ignore_index=True)

    translated_qdf.to_csv("question_translations.csv")
    

def retrieve_10_translations(number: int, text: str, languages):
    # a dictionary of all the translations
    temp = {}
    temp["en"] = text
    
    for lan in languages:
        temp[lan] = lang_translation(question=text, lan=lan)
        print(f"Question {number} -- {lan} DONE ✅")
    
    return temp


if __name__ == "__main__":
    main()