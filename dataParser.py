

import csv,json
path = "C:/Users/Curly/Desktop/fuzzy/expert1.txt"


mapping = ['one','eqx','wkx','esx','vsx','abx','eqr','wkr','esr','vsr','abr']



def convertToJson(file):
	# Space in CSV File ??
	print('openfile' , file)
	content = open(file).read().replace(' ','')
	with open(file,'w') as f :
		f.write(content)
	maxLayer = 0 # Clean
	# Do your stuff
	with open(file) as csv_file :
		csv_reader = csv.DictReader(csv_file,delimiter=';')
		nodelist = {}
		for row in csv_reader :
			# Level should be an int
			matrix = []
			matrixString = row['Matrix'].replace('{','').replace('}','')
			matrixRow = matrixString.split('],[')
			for r in matrixRow : #  [(one),(one),(wkx)
				r = r.replace('[','').replace(']','').replace('(','').replace(')','')
				# one,one,wkx
				fuzzyStr = r.split(',')
				l = []
				for fuzzy in fuzzyStr :
					l.append(mapping.index(fuzzy))
				matrix.append(l)
			child =  row['Child'].replace('{','').replace('}','').split(',')
			if child == ['ATLS']:
				child = []
				manufacturerCount = len(matrix[0]) # Clean
				for i in range(len(matrix[0])):
					child.append('ATLS'+str(i))
			maxLayer = max(int(row['Level']),maxLayer)
			nodedata = {
				"Level" : int(row['Level']),
				"Child" :child,
				"Matrix" : matrix
			}
			nodelist[row['Name']] = nodedata


		maxLayer += 1
		for i in range(manufacturerCount):
			nodedata = {
				"Level" : maxLayer,
				"Child" : [],
				"Matrix" : []
			}
			nodelist['ATLS' + str(i)] = nodedata
		

		return nodelist
		
def convertToTree(jsonData):
	import copy
	jsonData = copy.deepcopy(jsonData)
	
	startNode = None
	maxLevel = 0
	for node, data in jsonData.items():
		if data['Level'] == 0 :
			startNode = node
		maxLevel = max(maxLevel,data['Level'])
	jsonData["ATLS"] = {"Level" : maxLevel + 1}
	for currentLevel in range(maxLevel,-1,-1) :
		for node, data in jsonData.items():
			if data['Level'] != currentLevel :
				continue
			newChild = {}
			for i in range(len(data['Child'])):
				newChild[data['Child'][i]] = jsonData.__getitem__(data['Child'][i])
			jsonData[node]['Child'] = newChild
	
	listKey = list(jsonData.keys())
	listKey.remove(startNode)
	for key in listKey :
		del jsonData[key]

	result = {
		'data' : jsonData,
		'flatten' : flatten(jsonData,maxLevel)
	}

	return jsonData
			



def flatten(origin,layerCount,temporary=None):
	for currentLayer in range(layerCount):
		print('layer' , currentLayer)





		
	# completed = False
	# while not completed :
	#     completed = True
	#     for node,data in jsonData.items():
	#         if data :
	#             for child in data['Child']:
	#                 if isinstance(child,str) :
	#                     completed = False
	#                     temp = child
	#                     if child == "ATLS" :
	#                         child = {"ATLC" : None}
	#                         continue
	#                     child = jsonData[child]
	#                     jsonData[temp] = None
	#     # Clean 'z
	#     for node in jsonData[startNode]["Child"] :
	#         try :
	#             del jsonData[node]
	#             print('del'  , node)
	#         except :
	#             pass


# Flat a tree so that we can assign the position of each node
# Return [ ["A"] ,[ ["C"] , ["F"]]  , ["B"]]


	
# def generateTreeData(database):
#     listNode = []
#     for node , data in database.items():
#         newNode = NodeData(
#             name = node,
#             childs = data['Child'],
#             matrix = data['Matrix'],
#             level = data['Level']
#         )
#         listNode.append(newNode)
#     # debug(listNode)


KW_MATRIX_SEP = ' vs '

class NodeData :
	def __init__(self,name='',data={'Matrix':[],'Level':-1,'Child':[]},scope=None,isManufacturer=False):
		print('[INFO] Create Node' , name)
		self.name = name
		self.matrix = data['Matrix']
		self.level = data['Level']
		self.child = []
		self.isManufacturer = isManufacturer
		if False :
			with open('scope.json' ,'w') as f :
				for node , data in scope.items():
					f.write(str(node)+'\t'+str(data) + '\n')

		for child in data['Child']:
			# if child.startswith('ATLS'):
			# 	self.child.append(child)
			# 	continue
			childObj = scope[child]
			self.child.append(childObj)
			childObj.parent = self

		self.parent = None
		
	@property
	def friend(self):
		return self.parent.child

	def __setitem__(self,index,value):
		# Set the value of # Barecost vs Money => matrix[0][1]
		arg = index.split(KW_MATRIX_SEP)
		child1 = None
		child2 = None
		for child in self.child :
			if child.name == arg[0]:
				child1 = self.child.index(child)
			if child.name == arg[1]:
				child2 = self.child.index(child)

		if child1 == None or child2 == None :
			raise ValueError('Cant find' , self.__str__() , arg)
		self.matrix[child1][child2] = value
		print('[TRACE]' , 'set value' , index , value )

	def __getitem__(self,index):
		child1 = None
		child2 = None
		# Set the value of # Barecost vs Money => matrix[0][1]
		arg = index.split(KW_MATRIX_SEP)
		for child in self.child :
			if child.name == arg[0]:
				child1 = self.child.index(child)
			if child.name == arg[1]:
				child2 = self.child.index(child)
		if child1 == None or child2 == None :
			raise ValueError('Cant find' , self.__str__() , arg)
		return self.matrix[child1][child2] 


	def sliderList(self):
		sliderLabel = {}
		dimension = len(self.child)
		if True:
			for x in range(dimension):
				for y in range(dimension):
					if x == y :
						continue
					name = self.child[x].name + KW_MATRIX_SEP + self.child[y].name
					sliderLabel[name] = self.matrix[x][y]
		
		return sliderLabel
		

	def __str__(self):
		selfdata = {}
		listKey = list(self.__dict__)
		for key,value in self.__dict__.items():
			if not key.startswith('__'):
				selfdata[key] = value
		return str(selfdata)

	def __repr__(self):
		return 'Node(' + self.name + ')'
		
def toEvn(path):
	allNodeJson = convertToJson(path)
	listNode = []
	maxLevel = 0
	for _ ,data in allNodeJson.items():
		maxLevel = max(maxLevel,data['Level'])
	for currentLevel in range(maxLevel+1,-1,-1):
		for node,data in allNodeJson.items():
			if data['Level'] == currentLevel :
				listNode.append([node,data])
				print('[DEBUG]' , data)
				
	
	allNode = {}
	for nodeData in listNode :
		newNode = NodeData(
			name = nodeData[0],
			data = nodeData[1],
			scope = allNode
		)
		allNode[nodeData[0]] = newNode
		print('[DEBUG]' , newNode, newNode.level)
		# print('add' , nodeData[0] , newNode)

	topNode = None
	for node  in listNode:
		if node[1]['Level'] == 0 :
			topNode = allNode[node[0]]
			print('topnode = ' , topNode)
			return topNode , allNode

def criteriaDumps(data):
	string = 'Name;Parent;Level;Child;Matrix\n'
	lines = []
	for key,value in data.items():
		if 'ATLS' in key :
			continue
		name = value.name
		parent = 'Root' if value.parent==None else value.parent.name
		level = str(value.level)
		child = '{ATLS}' if 'ATLS' in value.child[0].name else ('{' + ','.join([obj.name for obj in value.child]) + '}')
		matrix = str(value.matrix)
		for i in range(len(mapping)):
			matrix = matrix.replace(str(i),'(' + mapping[i] + ')' )
		matrix = '{' + matrix[1:-1] + '}'
		matrix = matrix.replace(' ','')
		lines.append( ';'.join([name,parent,level,child,matrix]) + '\n' )
	
	lines.reverse()
	return string + ''.join(lines)


	


	
