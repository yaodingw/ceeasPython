import re
import urllib.request
import urllib

#获取所有学校的网站
#http://data.api.gkcx.eol.cn/soudaxue/queryschool.html?messtype=jsonp&page=11
#base method
def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0')
    response = urllib.request.urlopen(req)
    return response.read()

def getHtml(page):
	data={}
	data['messtype']='jsonp'
	data['page']=page
	url_values=urllib.parse.urlencode(data)
	url="http://data.api.gkcx.eol.cn/soudaxue/queryschool.html?"
	full_url=url+url_values
	# print(full_url)
	data=url_open(full_url).decode('utf-8')
	return data

def saveDataFile(fileContent):
	path="..\\datatext\\allCollege\\allCollege.txt"
	with open(path,"a",encoding='utf-8') as f:
  		f.write(fileContent)

 #正则过滤显示所有的学校名
def regxGetCollegeName(html):
 	patter=re.compile(r'"schoolname.+?"(\w.+?)"',re.S)
 	return patter.findall(html)

#遍历所有的表格获取大学数据
def getAllCollege():
	j=0
	k=0
	for i in range(276):
		html_data=getHtml(i+1)
		if html_data:
			saveCollegeName=regxGetCollegeName(html_data)
			saveDataFile(html_data)
			for name in saveCollegeName:	
				k+=1			
				print(str(k)+"保存学校:"+name+"  到allCollege.txt文件.")
				j+=1
	print("共保存学校"+str(j)+"所!")

#################################
'''
读文件
'''
def getDataSource(sDataPath):
	with open(sDataPath,"r",encoding='utf-8') as f:
		return f.read()

if __name__ == '__main__':
	getAllCollege()
	# html=getDataSource("D:\\yaoding\\biyesheji\\dataSource\\datatext\\allCollege\\allCollege.txt")
	# print(regxGetCollegeName(html))