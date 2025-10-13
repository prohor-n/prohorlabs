import re
DIGITS = {'0':'ноль','1':'один','2':'два','3':'три','4':'четыре','5':'пять','6':'шесть','7':'семь','8':'восемь','9':'девять'}
def to_words(n): return ' '.join(DIGITS[d] for d in str(n))
def process(f):
    with open(f) as file: txt = file.read()
    pattern = re.findall(r'\b\d*2[0-3][13]\b', txt)
    valid = [x for x in pattern if int(x, 4) <= 4095]
    for x in valid: print(x.replace('2',''))
    if valid:
        decs = [int(x,4) for x in valid]
        print("Среднее (прописью):", to_words((min(decs)+max(decs))//2))
process("prohortest1.txt")
