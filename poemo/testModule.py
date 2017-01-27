import en
from settings import *

if __name__ == "__main__":
    text_file = text_dir+str(0)+".txt"
    text = read_text(text_file)
    summary = en.content.categorise(txt)
    print summary.primary
    print summary.secondary
    print summary.emotions
