import requests,re,json
from bs4 import BeautifulSoup

#データを取得してbsで扱える所まで加工
def htmlGetter(url):
	raw=requests.get(url)
	html=raw.text
	soup=BeautifulSoup(html)
	return soup
#いらない文字列などを消し、整形したものをres辞書に入れる
def defGetter(data,num):
	TF = re.split(r'"',str(data))
	if "resultsList" in TF:
		exp=data.find("div",{"id":"resultsList"})
		delete=exp.div.find_all("span")
		for w in delete:
			w.decompose()
		res[num]=[]#numはクリックした句動詞の番号
		res[num].append(str(exp.li.span.get_text()))
		res[num].append(str(exp.div))
		return res
	else:
		res[num]=[]
		res[num].append("no match")
		return res

#作業に入る準備、句動詞番号と、検索キーワードをファイルから取得
f=open("list_en.csv","r")
arryRows,i=[],0
arry=[line.rstrip('\n') for line in f]
f.close()
while(i<len(arry)):
	arryRows.append(arry[i].split(","))
	i+=1

#実際の作業
j=0
res={}	
while(j<len(arry)):
	if j==0 or j==len(arry)-1:
		j+=1
		continue
	else:
		srch_key=arryRows[j][1]+"+"+arryRows[j][2]
		url="http://eow.alc.co.jp/search?q=%22{0}%22".format(srch_key)
		soup=htmlGetter(url)
		res.update(defGetter(soup,j))
		j+=1

#整形されたデータが入った辞書resを保存。
f=open("definitions.json","w")
json.dump(res,f)
f.close()
