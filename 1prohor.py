DIGITS = {'0':'ноль','1':'один','2':'два','3':'три','4':'четыре','5':'пять','6':'шесть','7':'семь','8':'восемь','9':'девять'}
def to_words(n): return ' '.join(DIGITS[d] for d in str(n))
def is_q(num): return all(c in '0123' for c in num)
def process(f):
    with open(f) as file: data = file.read().split()
    nums = [int(x,4) for x in data if is_q(x) and int(x,4)%2==1 and int(x,4)<=4095 and len(x)>=3 and x[-3]=='2']
    for x in data:
        if is_q(x) and int(x,4)%2==1 and int(x,4)<=4095 and len(x)>=3 and x[-3]=='2':
            print(''.join(c for c in x if c != '2'))
    if nums: print("Среднее (прописью):", to_words((min(nums)+max(nums))//2))
process("prohortest1.txt")
