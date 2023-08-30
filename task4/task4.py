# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 18:36:44 2022

@author: Shengyu Sun
"""

from bs4 import BeautifulSoup
import requests
import urllib.request as url
from googlesearch import search
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


def url_create(p,q):
    url=[]
    for i in range(p,q):
        url.append(read_file.iloc[i,3])
    return url

def get_affiliation_labsize(PLOS_url,head):#get PLOS papers' affiliation university and lab size
    affiliation_uni=[]
    labsize=[]
    for i in PLOS_url:
        url="https://journals.plos.org/plosone/article?id="+i
        content=requests.get(url,headers=head,timeout=30)
        text=content.text
        bs=BeautifulSoup(text,'html.parser')
        lab=len(bs.find_all("li",{"data-js-tooltip":"tooltip_trigger"}))
        affiliation=bs.find_all('meta',{'name':'citation_author_institution'})[0]['content']
        labsize.append(lab)
        affiliation_uni.append(affiliation)
    return affiliation_uni,labsize

#----------------------------get information form pubmed
def get_med_link(title,head):#get paper links in pubmed
    links = []
    for i in title:
        url="https://pubmed.ncbi.nlm.nih.gov/?term=" + i.replace(" ","+")
        content=requests.get(url,headers=head,timeout=30)
        text=content.text
        bs=BeautifulSoup(text,'html.parser')
        link = bs.find("button", {"class":"share-search-result trigger result-action-trigger share-dialog-trigger"})
        if link == None:
            value = url
        else:
            value = link["data-permalink-url"]
        links.append(value)
    return links

def get_affiliation_labsize_med(links,head):
    affiliation_uni=[]
    labsize=[]
    for i in links:
        content=requests.get(i,headers=head,timeout=30)
        text=content.text
        bs=BeautifulSoup(text,'html.parser')
        lab=len(bs.find_all('span',{'class':'authors-list-item'}))
        labsize.append(lab)
        affiliations=bs.find('a',{'class':'affiliation-link'})
        if affiliations != None:
            affiliation=affiliations.get('title')
        affiliation_uni.append(affiliation)
    return affiliation_uni,labsize
#-----------------------------end section of getting information from pubmed

def get_author_list(df):
    author_list=df.Authors.apply(lambda x:x.split(',')[0]).tolist()
    return author_list

def get_degree_area(titles):
    degree_list=[]
    area_list=[]
    driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    for i in titles:
        curr_page = 'https://www.researchgate.net/search/publication?q='+i
        print(i)
        driver.get(curr_page)
        driver.implicitly_wait(1)
        try:
            driver.find_element(By.CLASS_NAME, "nova-legacy-v-person-inline-item__fullname").find_element(By.XPATH, "./..").click()#模拟浏览器动作，点击第一作者
            driver.implicitly_wait(1)
            resp=driver.page_source
            bs_test=BeautifulSoup(resp,'html.parser')
            if bs_test.find_all('h5',{'class':'nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-s nova-legacy-e-text--color-grey-400'})!=[]:
                degree_list.append('N/A')
                area_list.append('N/A')
            else:
                try:
                    degree=bs_test.find_all('div',{'class':'nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-600 title'})[0].contents
                    if type(degree)==list:
                        degree=degree[0].split(',')[0]
                    if 'of' in degree:
                        area=degree[degree.index('of')+3:]
                    else:
                        if 'in' in degree:
                            area=degree[degree.index('in')+3:]
                        else:
                            area='N/A'
                except Exception as e:
                    degree='N/A'
                    area='N/A'
                degree_list.append(degree)
                area_list.append(area)
        except Exception as e:
            degree_list.append('N/A')
            area_list.append('N/A')
    return degree_list,area_list

def get_journalNumber_duration_publicationRate(author_list):    
    journal_number_list=[]
    duration_list=[]
    rate_list=[]
    for i in author_list:
        print(i)
        url="https://pubmed.ncbi.nlm.nih.gov/?term="+i
        content=requests.get(url,headers=head,timeout=30)
        text=content.text
        bs=BeautifulSoup(text,'html.parser')
        if bs.find_all('div',{'class': 'results-amount'})==[]:
            duration_list.append('N/A')
            rate_list.append('N/A')
            journal_number_list.append(1)
        else:
            if bs.find_all('div',{'class': 'results-amount'})[0].contents==['\n  \n    No results were found.\n  \n']:
                journal_number_list.append(1)
                duration_list.append('N/A')
                rate_list.append('N/A')
            else:
                journal_number=bs.find_all('meta',{'name': 'log_resultcount'})[0]['content']
                journal_number=int(journal_number)
                pub_time=[]#定义一个存放发表论文时间的list
                if journal_number>300:
                    journal_number=300#这个网站没有对姓名进行去重，有的作者有6000多篇，所以为了避免程序过载，加个限制
                for j in range(1,int(journal_number/10)+2):#这里用来解决翻页问题，同时爬取每篇文章发表的年份
                    url_temp=url+'&page='+str(j)
                    content_temp=requests.get(url_temp,headers=head,timeout=30)
                    text_temp=content_temp.text
                    bs_temp=BeautifulSoup(text_temp,'html.parser')
                    for x in bs.find_all('span',{'class':'docsum-journal-citation short-journal-citation'}):
                        try:
                            pub_time.append(int(x.contents[0][-5:-1]))#到这里结束
                        except Exception as e:
                            pass
                duration=max(pub_time)-min(pub_time)
                duration_list.append(duration)
                if duration==0:
                    publication_rate=1
                else:
                    publication_rate=journal_number/duration
                rate_list.append(publication_rate)
                journal_number_list.append(journal_number)
    return journal_number_list,duration_list,rate_list


if __name__ == '__main__':
    head = {'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166' }
    read_file=pd.read_csv('bik.csv',encoding = "ISO-8859-1",sep='\t')
    read_file=read_file.iloc[:214,:]
    PLOS_url=url_create(0,48) #fetch papers from PLOS.org
    med_url=url_create(48,214)#fetch papers from pubmed
    title_med = []
    for i in range(49,214):
        title_med.append(read_file.iloc[i,1])#fetch titles
    med_url = get_med_link(title_med,head)
    #get affiliation from PLOS and pubmed:
    affiliation_uni_PLOS,labsize_PLOS=get_affiliation_labsize(PLOS_url,head)
    print('get plos affiliation')
    affiliation_uni_med,labsize_med=get_affiliation_labsize_med(med_url,head)
    print('get med affiliation')
    author_list=get_author_list(read_file)[0:]
    
    titles=read_file[0:]['Title'].tolist()
    degree_list_0_132,area_list_0_132=get_degree_area(titles[0:132])
    print('get 132 degree and area')
    degree_list_132,area_list_132=get_degree_area(titles[132:])
    print('get total degree and area')
    degree_list=degree_list_0_132+degree_list_132
    area_list=area_list_0_132+area_list_132
    
    journal_number_list_0_126,duration_list_0_126,rate_list_0_126=get_journalNumber_duration_publicationRate(author_list[0:126])
    journal_number_list_126,duration_list_126,rate_list_126=get_journalNumber_duration_publicationRate(author_list[126:])
    journal_number_list=journal_number_list_0_126+journal_number_list_126
    duration_list=duration_list_0_126+duration_list_126
    rate_list=rate_list_0_126+rate_list_126
    
    print('get journalnumber')
    affiliation=affiliation_uni_PLOS+affiliation_uni_med
    labsize=labsize_PLOS+labsize_med
    read_file['affiliatiom']=affiliation
    read_file['labsize']=labsize
    read_file['highest degree']=degree_list
    read_file['career duration']=duration_list
    read_file['journal number']=journal_number_list
    read_file['publication rate']=rate_list
    read_file.to_excel('author_result.xlsx')











