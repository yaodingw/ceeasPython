import re
import urllib.request
import urllib
import threading
import time
#定义一个自定义栈
class Stack: 
    """模拟栈""" 
    def __init__(self,data): 
        self.items = data[::]
 
    def isEmpty(self): 
        return len(self.items)==0  
 
    def push(self, item): 
        self.items.append(item) 
 
    def pop(self): 
        return self.items.pop()  
 
    def peek(self): 
        if not self.isEmpty(): 
            return self.items[len(self.items)-1] 
 
    def size(self): 
        return len(self.items) 

#遍历所有学校,从用学校名字去请求该学校的所有的分数线

def getCollegeName():
	sDataPath="D:\\yaoding\\biyesheji\\dataSource\\datatext\\allCollege\\allCollege.txt"
	data=""
	with open(sDataPath,"r",encoding='utf-8') as f:
		data=f.read()
	patter=re.compile(r'"schoolname.+?"(\w.+?)"',re.S)
	return patter.findall(data)

def getAllPage(html):
	patter=re.compile(r'"totalRecord".+?num.+?"(\d.+?)"',re.S)
 	return patter.findall(html)

def printCollegeSL(html):
	yearPatter=re.compile(r'"year.+?(\d.+?)"',re.S)
	scorePatter=re.compile(r'"var_score.+?(\d.+?)"',re.S)
	ys=[]
	year=yearPatter.findall(html)
	score=scorePatter.findall(html)
	ys.append(year)
	ys.append(score)
	return print(ys)

#根据学校的名字来保存分数
def saveDataFile(name,fileContent):
	path="..\\datatext\\allCollege\\allCollegeSL\\"+name+".txt"
	try:
		with open(path,"a",encoding='utf-8') as f:
  			f.write(fileContent)
	except:
  		print(name+"error!")

def saveErrorCollege(name):
	path="..\\datatext\\allCollege\\errorCollege\\noSaveCollege.txt"
	try:
		with open(path,"a",encoding='utf-8') as f:
			f.write(name+"\r\n")
	except:
		print(name+"error!")


#provinceforschool=&schooltype=&page=1&size=10&keyWord=清华大学
def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0')
    response = urllib.request.urlopen(req)
    return response.read()

def getHtml(name,page=1):
	data={}
	data['messtype']='jsonp'
	data['url_sign']='queryProvinceScore'
	data['page']=page
	data['size']=50
	data['keyWord']=name
	url_values=urllib.parse.urlencode(data)
	url="http://data.api.gkcx.eol.cn/soudaxue/queryProvinceScore.html?"
	full_url=url+url_values
	# print(full_url)
	data=url_open(full_url).decode('utf-8')
	return data

collegeName=getCollegeName()
stackName=Stack(collegeName)
#线程类
class myThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.lock = threading.Lock()
	def run(self):

		while True:
			print("thread"+self.name)
			self.lock.acquire()
			if stackName.size()>0:
				name=stackName.pop()
			else:
				return print("学校各地区分数线获取完毕!")
			self.lock.release()	
			startSaveCollege(name)
			print("thead"+self.name+"保存"+name+"完成!进入睡眠!")
			time.sleep(2)
			


def startSaveCollege(name):
	print(name)
	#对学校栈加锁
	k=0
	correctNum=0
	html=getHtml(name)
	time.sleep(2)
	try:
		amount=int(getAllPage(html)[0])
		page=int(amount/50)
		print(name+":总条数"+str(amount)+",总页数"+str((page+1)))
	except:
		print(name+"获取总条数异常!")
		# pass "保存异常的学校的名字到exceptionName.txt"
		saveErrorCollege(name)
		return None
	if amount%50>0:
		page+=1
	for curPage in range(page):
		html=getHtml(name,curPage+1)
		saveDataFile(name,html)
	print(name+":各个地区分数线保存成功!保存地址"+"D:\\yaoding\\biyesheji\\dataSource\\datatext\\allCollege\\allCollegeSL"+name+".txt")

def main():
	collegeName=getCollegeName()
	#collegeName=['清华大学']
	k=0
	errorNum=0
	correctNum=0
	for name in collegeName:
		html=getHtml(name)
		try:
			amount=int(getAllPage(html)[0])
			page=int(amount/50)
			print(name+":总条数"+str(amount)+",总页数"+str((page+1)))
		except:
			errorNum+=1
			print(name+"获取总条数异常!")
			# pass "保存异常的学校的名字到exceptionName.txt"
			saveErrorCollege(name)
			continue
		if amount%50>0:
			page+=1
		for curPage in range(page):
			html=getHtml(name,curPage+1)
			saveDataFile(name,html)
		k+=1
		correctNum+=1
		print(str(k)+name+":各个地区分数线保存成功!保存地址"+"D:\\yaoding\\biyesheji\\dataSource\\datatext\\allCollege\\allCollegeSL"+name+".txt")	
	print("保存成功的学校有"+str(correctNum)+"所!\r\n"+"没有保存成功的学校有"+str(errorNum)+"所")




if __name__ == '__main__':
	# thread1 = myThread(1, "Thread-1", 1)
	# thread2 = myThread(2, "Thread-2", 2)

	# # 开启新线程
	# thread1.start()
	# thread2.start()
	name=''
	for i in range(15):
		name="thread"+str(i)
		name=myThread(i,i,i)
		name.start()


