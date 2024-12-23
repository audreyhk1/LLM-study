import pandas as pd

def main():
    # get all medical questions
    qdf = pd.read_csv("data/qdf.csv")
    print(qdf)
    
    
if __name__ == "__main__":
    main()