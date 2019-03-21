# -- coding:utf-8 --

from urllib import request
from html.parser import HTMLParser
import re, json

class MyHtmlParser(HTMLParser):
    tempstr = str()
    liststr = ""
    def handle_starttag(self, tag, attrs):
        if tag == 'center':
            self.tempstr = ''
            
    def handle_endtag(self, tag):
        if tag == 'center':
            matchObj = re.search(r'(\d*)\.(\d*)\.(\d*)\.(\d*)', self.tempstr)
            if matchObj:
                self.liststr = matchObj.group()
                
    def handle_data(self, data):
        if(data.isspace() == False):
            self.tempstr += data

def query():			
	url = r'http://2019.ip138.com/ic.asp'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

	req = request.Request(url=url, headers = headers)
	res = request.urlopen(req)
	data = res.read().decode('gbk')

	parser = MyHtmlParser()
	parser.feed(data)
	
	return parser.liststr
	
def getWanIp(url):
    res = request.urlopen(url)
    data = json.loads(res.read().decode('utf8'))

    if data['code'] == 0:
        return data['data']['ip']
    else:
        return None



#for value in liststr:
#    print(value)

#print(liststr[0])
