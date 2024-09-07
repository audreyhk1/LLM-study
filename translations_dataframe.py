import pandas as pd
from translate_libraries.final_translate import lang_translation
from dataframe import create_question_dataframe

def main():
    df = create_question_dataframe()
    print(df)
    


if __name__ == "__main__":
    main()