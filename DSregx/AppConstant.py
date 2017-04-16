from enum import Enum

#地区代码号
#从文件获取爬虫爬到的数据
def getDataSource(sDataPath):
	with open(sDataPath,"r",encoding='utf-8') as f:
		return f.read()
 

 #获取个地区分数线的函数
def getPSL(sData):
	pslPattern=re.compile(r'',re.S)
	res=pslPattern.findall(sData)


#把字符串保存到文件中
def saveDataFile(fileName,fileContent):
	path="..\\datatext\\"+fileName
	with open(path,"w",encoding='utf-8') as f:
  		f.write(fileContent)