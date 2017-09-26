#coding=utf-8

import re
import urlparse
import time
import urllib2
from bs4 import BeautifulSoup

#from neo4j.v1 import GraphDatabase, basic_auth
from py2neo import Graph,Node,Relationship,NodeSelector

def getDB():
     return Graph(
            "http://127.0.0.1:7474", 
            username="neo4j", 
            password="vnique"
        )

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
        
    def craw(slef,g):
        root_url = g['url']
        html_content = slef.download(root_url)
        soup1 = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        pages_num = soup1.find('div',class_="turnPageBottom").find('span',class_="pageOp").get_text()[1:3]
        print(pages_num)
        time.sleep(3)
        #print type(links_1)
        
        graphDB = getDB()
        
        for i in range(1, int(pages_num) + 1):
            print(i)
            new_url=root_url.replace('j1','j'+str(i))
            print(new_url)
            html_content2 = slef.download(new_url)
            soup2 = BeautifulSoup(html_content2, 'html.parser', from_encoding='utf-8')
            links_1 = soup2.find('div',class_="itemSearchResult clearfix fashionList").find_all('li')
            print len(links_1)
            for item in links_1:
                url_product=item.find('a',class_="product_pic pro_img")['href']
                print(url_product)
                html_content3 = slef.download(url_product)
                soup3 = BeautifulSoup(html_content3, 'html.parser', from_encoding='utf-8')
               
                business_name=soup3.find('div',class_="middle_property").find('span').get_text()
                
                if business_name =='商家':
                    bus_link=soup3.find('div',class_="right_property")
                    bus_link_1=bus_link.find_all('a')
                    if len(bus_link_1)==2:
                        bus_name=bus_link_1[0].get_text()
                        bus_url=bus_link_1[0]['herf']
                        bus_yingyezhizhao=bus_link_1['herf']
                    info_bus=bus_link.find('ul',class_="info_list").find_all('span')
                    for item in info_bus:
                        print(item.get_text())
                else:
                    print '自营'
               
                keys  = soup3.find('div', class_="goods_intro").find_all('th')
                values  = soup3.find('div', class_="goods_intro").find_all('td')
                print len(keys)
                print len(values)
                
                find_1 = graphDB.find_one("Product_111", property_key="name",property_value=values[0].get_text())
                if not find_1:
                    if len(keys)==len(values):
                        n = len(keys)
                    else:
                        n = min(len(keys),len(values))
                    print '1111111111111111'
                    node = Node("Product_111",name = values[0].get_text())
                    for i in range(1,n):
                        node[keys[i].get_text()] = values[i].get_text()
                    graphDB.create(node)
                    node_belongto_g = Relationship(node,'相关药品',g)
                    graphDB.create(node_belongto_g)
                    g_belongto_node = Relationship(g,'适用于',node)
                    graphDB.create(g_belongto_node)
                else:
                    print find_1
                    
                #res_data['title'] = title_node[0].get_text()
                #res_data['pinpai'] = title_node[1].get_text()
                #res_data['guige'] = title_node[2].get_text()
                #res_data['zhongliang'] = title_node[3].get_text()
                #res_data['changshang'] = title_node[4].get_text()
                #res_data['wenhao'] = title_node[5].get_text()
                                                              
    def get_categorys(self):
        graphDB = getDB()
        selector = NodeSelector(graphDB)
        find_one = selector.select("Category_111",completed=0)
        #find_c = graphDB.data("MATCH (a:Category_111) where a.completed = 0 RETURN a.url")
        return find_one
            
               

if __name__ == '__main__':
    # 爬虫入口页面
    #root_url = 'http://www.111.com.cn/categories/965143-j1.html'
    obj_spider = SpiderMain()
    # 启动爬虫
    #
    graphDB = getDB()
    gs = list(obj_spider.get_categorys())
    if len(gs)>0:
        gs[0]['completed'] = 1
        graphDB.push(gs[0])
        obj_spider.craw(gs[0])
        
