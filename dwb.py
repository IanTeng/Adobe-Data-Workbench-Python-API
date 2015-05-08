# -*- coding: utf-8 -*- 
#Copyright (c) 2015 - Ian <dengxw@eship.com.cn> 

'''
#python wrapper for adobe data workbench api
    
#function:
__init__(self,server,profile)
createRequest(self,query):
resultRequest(self,queryId,completion=0,format='json')
dropRequest(self,queryId):
getSchema(self,format='text'):
 
#value option:
server:
    insight server,example:"127.0.0.1:81"
profile:
    insight profile name,example:"My Profile"
query:
    query expression,example:"eval Visits over Day;" 
format:
    data return format,including json,text and xml
completion:
    query completion(sample rate)
    value range from 0.0-1.0

 
#Usage:
import dwb
#init client
client=dwb.DwbClient('192.168.16.222:81','Plateno Prd')
#create query and get queryid
queryId=client.createRequest('eval Visits over Day;')
#get query result
result=client.resultRequest(queryId)
'''

import requests
import urllib
import logging

logging.basicConfig(filename='dwb_api.log',level=logging.WARNING,format='%(asctime)s %(message)s')


class DwbClient:
    def __init__(self,server,profile):
        self.url='http://'+server+'/Profiles/'+urllib.quote(profile)+'/API.query'
        self.cHeaders={"X-Action":"create","X-Language":"Expression"}

    def createRequest(self,query):
        r=requests.post(self.url,headers=self.cHeaders,data=query,stream=False)
        return r.headers['X-Query-ID'] if r.status_code==200 else None

    def resultRequest(self,queryId,completion=0,format='json'):
        self.qHeaders={"X-Action":"result","X-Format":format,"X-Language":"Expression","X-Completion":completion,"X-Query-ID":queryId}
        r=requests.post(self.url,headers=self.qHeaders,stream=False)
        if r.status_code!=200:
            logging.warning('Create Query Failed:'+str(r.status_code)+str(r.headers))
        return r.content if r.status_code==200 else None
 
    def dropRequest(self,queryId):
        self.qHeaders={"X-Action":"drop","X-Query-ID":queryId}
        r=requests.post(self.url,headers=self.qHeaders,stream=False)
        if r.status_code!=200:
            logging.warning('Drop Request Failed:'+str(r.status_code)+str(r.headers))
        return True if r.status_code==200 else False 
        
    def getSchema(self,format='text'):
        self.sHeaders={"X-Action":"get-schema","X-Format":format}
        r=requests.post(self.url,headers=self.sHeaders,stream=False)
        if r.status_code!=200:
            logging.warning('Schema Fetch Failed:'+str(r.status_code)+str(r.headers))
        return r.content if r.status_code==200 else None 
        
