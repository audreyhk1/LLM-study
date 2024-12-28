import pytest
from chatgpt_rewordings import get_ChatGPT_rewording

def test_get_ChatGPT_rewording():
    q = get_ChatGPT_rewording("A 5-year-old girl is brought to the emergency department because of a 2 -day history of fever, urinary urgency, and burning pain with urination. She has had four similar episodes during the past year. A diagnosis of urinary tract infection is made. Subsequent renal ultrasonography shows one large U -shaped kidney. Which of the follo wing is the most likely embryologic origin of this patient's condition?")
    print(q)
    
