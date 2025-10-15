# нечетные четырехричные числа не превышающие 4095 в десятичной у которых третья справа цифра 2
import re
DIGITS = {'0':'ноль','1':'один','2':'два','3':'три','4':'четыре','5':'пять','6':'шесть','7':'семь','8':'восемь','9':'девять'}
def to_words(n): return ' '.join(DIGITS[d] for d in str(n))
def process(f):
    with open(f) as file: txt = file.read()
    valid = [x for x in re.findall(r'\b\d*2[0-3][13]\b', txt) if int(x, 4) <= 4095]
    for x in valid: print(x.replace('2',''))
    if valid: print("Среднее (прописью):", to_words((int(min(valid),4)+int(max(valid),4))//2))
process("prohortest1.txt")



