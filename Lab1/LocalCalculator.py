import calculator as t

class LocalCalculator:
    
    def __init__ (self):
        pass

    def sum (self,m,n):
        return t.sum(m,n)
    
    def divide (self,m,n):
        return t.divide(m,n)


calc = LocalCalculator()

print(calc.sum(2,5))
print(calc.divide(10,5))