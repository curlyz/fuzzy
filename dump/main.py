from fuzzymath import *
from __func__ import *
from const import *

import json,sys
# with open('global.json','w') as f :
#     f.write(json.dumps(sys.modules,sort_keys=True,indent=4))


ListDataFileName = ['Supplier.txt']

ListRawData = {}
for dataFileName in ListDataFileName :
    filedata = readdata(dataFileName)
    print(filedata)
    # convert expression into fuzzy number
    # convert_value_from_dict(fuzzyTable,filedata)
    ListRawData[dataFileName] = filedata

ListRefindedData = normalize_expert(ListRawData)
for refindedData in ListRefindedData :
    refindedData.weight = weight_calculation(refindedData.matrix)
    print('============= {} ==============='.format(refindedData.name))
    print(refindedData.matrix)

for refindedData in ListRefindedData :
    print('=============== {} =============='.format(refindedData.name))
    print(refindedData.weight)  