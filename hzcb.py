#!/usr/bin/python
#-*-coding:utf-8-*-

import urllib,urllib2,re

class searchPerson:
    html = ""
    count = []
    names = []

    def __init__(self):
        self.getHTML()
                   
    def getHTML(self,page=1):
        search_url = 'http://apply.hzcb.gov.cn/apply/app/status/norm/person'
        params = {
                'pageNo': page
        }
        params = urllib.urlencode(params)
        resp = urllib2.urlopen(search_url, params)
        self.html = resp.read()
        self.count = re.findall(r"window.parseInt\(\'\d*\'",self.html)

    def getTotalCount(self):
        total = self.count[0]
        return re.findall(r"(\d{1,7})",total)[0]
   
    def getPageCount(self):
        page = self.count[1]
        return re.findall(r"(\d{1,7})",page)[0]
    
    def getPageNames(self):
        return re.findall(r"<td >(.*)</td>",self.html)

    def getAllNames(self):
        for i in range(1,int(self.getPageCount())+1):
#            print i
            self.getHTML(i)
            self.names += self.getPageNames()
        return self.names

    def searchName(self,name=''):
        if name in self.names:
            return self.names.index(name)
        else:
            return None

    def countName(self):
        nameDict = {}
        if self.names:
            for i in range(1,len(self.names),2):
                firstName = self.names[i].decode('utf-8')[:1].encode('utf-8')
                #print "firstName: ",firstName," name: ",self.names[i]
                if nameDict.has_key(firstName):
                    nameDict[firstName] += 1
                else:
                    nameDict[firstName] = 1
            return nameDict
        else:
            return None

if __name__ == '__main__':             
    s = searchPerson()
    i=2
    l = s.getAllNames()
    print u"total name ",s.getTotalCount()
    d = sorted(s.countName().items(),key=lambda d:d[1],reverse = True)
    num = 0
    for (k,v) in d:
        print k," : ",v
        num += v
    print num
    #print s.countName()
    #while(i < len(l) + 1):
    #    print i / 2,l[i-2],l[i-1]
    #    i += 2
    #n = s.searchName("王敏")
    #if n >= 0 :
    #    print "恭喜"
    #    print l[n-1],l[n]

