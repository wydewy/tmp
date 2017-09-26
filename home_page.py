#coding=utf-8  

import re
import urlparse
import time
import urllib2
from bs4 import BeautifulSoup

#from neo4j.v1 import GraphDatabase, basic_auth
from py2neo import Graph,Node,Relationship

class SpiderMain(object):
    def download(slef,url):
        """
        下载该页面
        :param url:
        :return:
        """
        if url is None:
            return None
        # 打开一个url,返回一个 http.client.HTTPResponse
        response = urllib2.urlopen(url)
        # 若请求失败
        if response.getcode() != 200:
            return None
        return response.read()
        
    def craw(slef,root_url):
        html_content = slef.download(root_url)
        soup1 = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        #links_1 = soup1.find('div',id="allCategoryHeader").find_all('li',class_="stitle")
        links_1 = soup1.find_all('li',class_="stitle")
        print len(links_1)
        print type(links_1)
        
        graphDB = Graph(
            "http://127.0.0.1:7474", 
            username="neo4j", 
            password="vnique"
        )
        
        for link in links_1:
            try:
                data_1=link.find('a').find('h4').get_text()
                print(data_1)
                
                links_2=link.find('div',class_="category").find_all('dl')
                for d_1 in links_2:
                    try:
                        data_2=d_1.find('dt').find('a').get_text()
                        print(data_2)
                        links_3=d_1.find('dd').find_all('a')
                        for e_m in links_3:
                            try:
                                data_3=e_m.get_text() 
                                url_3=e_m['href']
                                '''
                                driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "vnique"))
                                # basic auth with: driver = GraphDatabase.driver('bolt://localhost', auth=basic_auth("<user>", "<pwd>"))

                                db = driver.session()
                                db.run("CREATE ({name}:Category_111 {name: {name}, url: {url}})",{"name": data_3, "url": url_3})

                                db.close()
                                '''
                                node = Node("Category_111",name = data_3,url = url_3,completed=0)
                                graphDB.create(node)
                                print(data_3)
                                print(url_3)
                                
                            except Exception as err:
                                print(err)
                                continue
                    except Exception as err:
                        print(err)
                        continue
                   
            except Exception as err:
                print(err)
                continue
              
       
        
        
if __name__ == '__main__':
    
    # 爬虫入口页面
    root_url = 'http://www.111.com.cn/'
    obj_spider = SpiderMain()
    # 启动爬虫
    obj_spider.craw(root_url)