# Fuzzy Math Implementation
DIMENSION = 3
class Fuzzy :
    #__slots__ = [] # Uncomment this to run faster
    def __init__(self,data=None):
        if data :
            self.array = data
        else :
            self.array = [0] * DIMENSION

    def __add__(self,other):
        return Fuzzy([self.array[i] + other.array[i] for i in range(DIMENSION)])

    def __mul__(self,other):
        return Fuzzy([self.array[i] * other.array[i] for i in range(DIMENSION)])
     
    def __sub__(self,other):
        if self.array[1] - other.array[1] < 0 :
            raise ValueError("Can't __sub__ between {} and {}".format(self,other))
        return Fuzzy([self.array[i] - other.array[abs(DIMENSION-i-1)] for i in range(DIMENSION)])

    def __truediv__(self,other):
        return Fuzzy([self.array[i] / other.array[abs(DIMENSION-i-1)] for i in range(DIMENSION)])
    
    def __invert__(self):
        return Fuzzy([1/self.array[i] for i in range(DIMENSION-1,-1,-1)])

    def __pow__(self,other):
        return Fuzzy([self.array[i]**other.array[i] for i in range(DIMENSION)])
    
    def __eq__(self,other):
        return all([self.array[i]==other.array[i] for i in range(DIMENSION)])
    
    def __int__(self):
        return sum(self.array) / DIMENSION

    def __repr__(self):
        return str(self.array)

    def __str__(self):
        return str([round(value,4) for value in self.array])
        

    def __contains__(self,valule):
        pass

    def __lt__(self,other):
        pass

    def __gt__(self,other):
        pass