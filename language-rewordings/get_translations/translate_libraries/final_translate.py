from .my_deepl_translate import deepl_translate
from .cloud_translate import translate_cloud

"""
F(x) rewords the question through converting it into a different language and changing it back 

Checks if returns the same string and saves as an error
"""
def lang_translation(question: str, lan: str):
    lang_translation = deepl_translate(text=question, translate_lan=lan)
    en_translation = translate_cloud(language=lan, text=lang_translation)
    
    if question == en_translation:
        raise "ERROR: no change occured in the question"
    else:
        return en_translation
    

def main():
    question = """
    A 50 -year-old man comes to the office because of a 2 -month history of increasing daytime somnolence. He has
    obstructive sleep apnea for which he has only intermittently used a continuous positive airway pressure device. He is
    170 cm (5 ft 7 in) tall and we ighs 181  kg (400 lb); BMI is 63  kg/m2. His temperature is 37°C  (98.6°F), pulse is 100/min,
    respirations are 12/min, and blood pressure is 135/80  mm Hg. Physical examination shows a gray -blue tinge to the lips,
    earlobes, and nail beds. Cardiac examination s hows no other abnormalities. Arterial blood gas analysis on room air
    shows a pH of 7.31, P CO2 of 70  mm Hg, and P O2 of 50 mm Hg. Which of the following additional findings would be
    most likely in this patient?
    """
    
    ## DEEPL - https://developers.deepl.com/docs/resources/supported-languages
    ## CLOUD - https://cloud.google.com/translate/docs/languages ---
    print(lang_translation(question=question, lan="nl"))
    
if __name__ == "__main__":
    main()