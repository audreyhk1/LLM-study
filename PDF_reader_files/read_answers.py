import pandas as pf
from pypdf import PdfReader
import sys

def main():
    DATA = "data/Step_1_Sample_Items (1).pdf"
    TXT = "data/answers.txt"
    
    pdf_to_txt(page=53, filename=DATA, txt=TXT)

def pdf_to_txt(page: int, filename, txt):
    """
    Opens a PDF and reads it page by page
    Write string on text file
    """
    reader = PdfReader(filename)
    
    with open(txt, "w") as file:
        file.write(str(reader.pages[page].extract_text()))
            
if __name__ == "__main__":
    main()