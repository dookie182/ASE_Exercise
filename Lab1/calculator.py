#calculator.py

def sum(m,n):

    if n < 0:
        for i in range(abs(n)):
            m = m - 1
        return m
    else: 
        for i in range(n):
            m = m + 1
        return m 

def divide(m,n):
    i = 0
    r = 0 

    if(n > m):
        return 0

    while m > 0 :
        m = m - n 
        i = i + 1
        r = m
    
    if r == 0:
        return i
    else:
        return i-1

if __name__ =="__main__":
    print(sum(1,5))
    print(divide(10,5))

