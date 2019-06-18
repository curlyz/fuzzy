

from fuzzymath import Fuzzy

fuzzyTable = {
    'one': Fuzzy( [1,1,1] ),
    'eqx': Fuzzy( [1,1,3] ),
    'wkx': Fuzzy( [1,3,5] ),
    'esx': Fuzzy( [3,5,7] ),
    'vsx': Fuzzy( [5,7,9] ),
    'abx': Fuzzy( [7,9,9] ),
    'eqr': ~Fuzzy( [1,1,3] ),
    'wkr': ~Fuzzy( [1,3,5] ),
    'esr': ~Fuzzy( [3,5,7] ),
    'vsr': ~Fuzzy( [5,7,9] ),
    'abr': ~Fuzzy( [7,9,9] )

}

print(fuzzyTable)