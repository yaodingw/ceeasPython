import os
#college_cutoff
#get all file collegecutoff
def findCollegeCutOff(path):
	for x in os.listdir(path):
		print(os.path.splitext(x)[0])

		
def getDataSource(sDataPath):
	with open(sDataPath,"r",encoding='utf-8') as f:
		return f.read()


def main():
	path="/home/wangyd/yaodingwork/biyesheji/dataSource/datatext/allCollege/allCollegeSL"
	findCollegeCutOff(path)

if __name__ == '__main__':
	main()