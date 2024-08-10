"""
creates thesaurus function (which should be imported into other py files):

access thesaurus api and converts every three words into synonym (10x) -> returns a list 
index node is always the original
"""
# Google translate
from google.cloud import translate

def thesaurus(question):
    return