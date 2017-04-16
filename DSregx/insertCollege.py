import re

collegeKey=['schoolname','province','schooltype','schoolproperty','level','f985','f211','guanwang','membership','jianjie','clicks']
typeDict={"综合类":0,"理工类":1,"农林类":2,"医药类":3,"师范类":4,"语言类":5,"财经类":6,"体育类":7,"艺术类":8,"民族类":9,"军事类":10,"政法类":11,"其它":12}


#save new insert sql file
def insertCollegeSql():
	path="/home/wangyd/yaodingwork/biyesheji/dataSource/datatext/allCollege/allCollege.txt"
	data=""
	with open(path,"r",encoding='utf-8') as f:
		data=f.read()
	#print(data)
	#allCollege name学校名字
	schoolNamePatter=re.compile(r'"schoolname.+?"(\w.+?)"',re.S)
	schoolName=schoolNamePatter.findall(data)
	#allCollege province地区
	provincePatter=re.compile(r'"province".+?"(\w.+?)"',re.S)
	province=provincePatter.findall(data)
	#allCollege schooltype院校性质
	schoolTypePatter=re.compile(r'"schooltype".+?"(\w.+?)"',re.S)
	schooltype=schoolTypePatter.findall(data)
	#allCollege schoolproperty 院校类别综合类
	schoolpropertyPatter=re.compile(r'"schoolproperty".+?"(\w.+?)"',re.S)
	schoolproperty=schoolpropertyPatter.findall(data)
	#allCollege level是否是本科 
	levelPatter=re.compile(r'"level".+?"(\w.+?)"',re.S)
	level=levelPatter.findall(data)
	#allCollege f985 IS985
	f985Patter=re.compile(r'"f985".+?"(\d)"',re.S)
	f985=f985Patter.findall(data)
	#allCollege f211 IS211 
	f211Patter=re.compile(r'"f211".+?"(\d)"',re.S)
	f211=f211Patter.findall(data)
	#allCollege guanwang url
	guanwangPatter=re.compile(r'"guanwang".+?"(.+?)"',re.S)
	guanwang=guanwangPatter.findall(data)
	#是否教育部直属
	membershipPatter=re.compile(r'"membership".+?"(.+?)"',re.S)
	membership=membershipPatter.findall(data)
	#简介
	lizi="jianjie"
	regx='"'+lizi+'".+?"(.+?)"'
	jianjiePatter=re.compile(regx,re.S)
	jianjie=jianjiePatter.findall(data)
	print(regx)
	print(jianjie)
	print(len(jianjie))


#获取插入COLLEGE_INFO的数据对象
def getInsertObject():
	#返回的dict集合对象
	collegeInfo={}
	path="/home/wangyd/yaodingwork/biyesheji/dataSource/datatext/allCollege/allCollege.txt"
	data=""
	with open(path,"r",encoding='utf-8') as f:
		data=f.read()
	#要遍历的key值
	for var in collegeKey:
		regx='"'+var+'".+?"(.+?)",'
		patter=re.compile(regx,re.S)
		proList=patter.findall(data)
		collegeInfo[var]=proList
	return collegeInfo

#创建插入COLLEGE_INFO表的insert语句
def saveCollegeInfoFile(collegeInfo):
	#declare variable
	name="";logo="";province="";level="";nType="";zhishu="";is211="";is985="";tel=""
	address="";email="";url="";remark="";seq=""
	#拼接insert语句
	for i in range(len(collegeInfo["schoolname"])):
		name=collegeInfo["schoolname"][i];logo=" "
		province=collegeInfo["province"][i];level=collegeInfo["schooltype"][i]
		nType=collegeInfo["schoolproperty"][i];zhishu=collegeInfo["membership"][i]
		if "教育部" in zhishu:
			#1 ==true
			zhishu=1
		else:
			zhishu=0
		if "本科" in level:
			level=1
		else:
			level=0
		nType=typeDict.get(nType,12)
		is211=collegeInfo["f211"][i];is985=collegeInfo["f985"][i]
		tel=" ";address="暂空";email=" ";url=collegeInfo["guanwang"][i]
		remark=collegeInfo["jianjie"][i];seq=collegeInfo["clicks"][i]
		sql="insert into COLLEGE_INFO (NAME,LOGO,PROVINCE,LEVEL,TYPE,ZHISHU,IS211,IS985,TEL,ADDRESS,EMAIL,URL,REMARK,SEQ) values ('"+name+"','"+logo+"','"+province+"',"+str(level)+","+str(nType)+","+str(zhishu)+","+str(is211)+","+str(is985)+",'"+tel+"','"+address+"','"+email+"','"+url+"','"+remark+"',"+seq+");\n\r"
		saveDataFile(sql)
		print(sql)



def saveDataFile(fileContent):
	path="/home/wangyd/yaodingwork/biyesheji/ceeasDB/insertCollegeInfo.sql"
	with open(path,"a",encoding='utf-8') as f:
  		f.write(fileContent)


def main():
	collegeInfo=getInsertObject()
	saveCollegeInfoFile(collegeInfo)

if __name__ == '__main__':
	main()
