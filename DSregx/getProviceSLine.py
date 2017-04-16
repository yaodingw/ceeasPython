import re
import urllib.request
import urllib

#地区数据编号
District=['北京','天津','上海','重庆','河北','河南','山东','山西','安徽','江西','江苏','浙江','湖北','湖南','广东','广西','云南','贵州','四川','陕西','青海','宁夏','黑龙江','吉林','辽宁','西藏','新疆','内蒙古','海南','福建','甘肃','港澳台']

#base method
def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0')
    response = urllib.request.urlopen(req)
    return response.read()


#用正则处理文本(处理地区录取分数线)
def regxHtml(all_the_html):
	#声明正则表达式
	#获取包含数据的div块
	pattern0=re.compile(r'( +?<div class="tabsContainer".*?</div)',re.S)
	#获取div块中td数据
	pattern1=re.compile(r'<td>([^<].+?)</td>',re.S)

	#处理第一个正则表达式
	target0=pattern0.search(all_the_html)
	if target0:
		targetData0=target0.group()

	#处理第二个正则表达式
	if targetData0:
		res=pattern1.findall(targetData0)

	return res

#获取页码
def getPage(all_the_html):
	pageList=[]
	pattern0=re.compile(r"<div.+?totalPage='(\d+?)' page='(\d+?)'></div>",re.S)
	# page=pattern0.findall(all_the_html)
	target=pattern0.search(all_the_html)
	if target:
		if target.group(1):
			pageList.append(target.group(1))
		if target.group(2):
			pageList.append(target.group(2))
	return pageList



#把处理好的数据切片,一行一行的保存到文件中
def addPSL(PList,cityCode):
	#向文件中累加保存数据
	def addSaveFilePSL(fileName,data):
		path="..\\datatext\\"+fileName
		with open(path,"a",encoding='utf-8') as f:
  			f.write(data)
	tarStr=''
	filename=District[cityCode]
	ext=".txt"
	for i in range(len(PList)):
		tarStr+=PList[i]
		if (i+1)%5==0:
			addSaveFilePSL(filename+ext,tarStr+"\r\n")
			print("保存数据:"+tarStr+"成功!")
			tarStr=''
		else:
			tarStr+=" "




def getHtml(local,page):
	data={}
	data['tab']='batch'
	data['local']=local
	data['page']=page
	url_values=urllib.parse.urlencode(data)
	url="http://kaoshi.edu.sina.com.cn/college/scorelist?"
	full_url=url+url_values
	# print(full_url)
	data=url_open(full_url).decode('utf-8')
	return data

#获取页码



#调用函数
def getCityScoreLine():
	html=""
	for i in range(31):
		#获取该地区第一页的数据
		html=getHtml(i+1,1)
		sumPage=getPage(html)[0]
		# print(sumPage)
		for j in range(int(sumPage)):
			html=getHtml(i+1,j+1)
			res=regxHtml(html)
			addPSL(res,i)



if __name__ == '__main__':
	getCityScoreLine()
	