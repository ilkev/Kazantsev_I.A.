from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import wget
import psycopg2
import re
s = Service('/Users/ilyaka/Desktop/chromedriver')
browser = webdriver.Chrome(service=s)
browser.get('https://music.yandex.ru/chart')
time.sleep (1)
html_text = browser.page_source
soup = BeautifulSoup(html_text, 'lxml')
track=soup.find_all('a', class_='d-track__title deco-link deco-link_stronger')
duration=soup.find_all('div', class_='d-track__info d-track__nohover')
author=soup.find_all('span', class_='d-track__artists')
pictures=soup.find_all('img', class_='entity-cover__image deco-pane')
str_pictures=[]
for i in range(len(pictures)):
    str_pictures.append(pictures[i])
str_pictures=str(str_pictures)
str_pictures=re.findall(r'src="(.*?)"',str_pictures)
for i in range(len(str_pictures)):
    str_pictures[i]='https:'+str_pictures[i]
#for i in range(len(str_cartinki)):
    #wget.download(str_cartinki[i], 'TOP'+str((i+1))+'.jpeg')


connection = psycopg2.connect(dbname = 'dbdata',
                           user='postgres', password='Q1w2e3r4',
                           host='localhost')
cursor=connection.cursor()
creat_table="""CREATE TABLE music
    (id serial primary key, "track" varchar(100),
    "duration" varchar(100),
    "author" varchar(100),
    "pictures" varchar(100))"""
cursor.execute(creat_table)
connection.commit()
for track, duration, author, pictures in zip(track, author, duration, pictures):
    qwery=f"""INSERT INTO public.music(
	    track, duration, author, pictures)
	    VALUES 
	    ('{track.text}','{duration.text}','{author.text}', '{pictures.text}' )"""
    cursor.execute(qwery)
    connection.commit()
for i in range(1,len(str_pictures)+1):
    puti = r'C:\Users\kingo\PycharmProjects\pythonProject2\TOP' + str(i) + '.jpeg'
    qwery=f"""UPDATE public.music
        SET pictures='{puti}'
        WHERE id={i}"""
    cursor.execute(qwery)
    connection.commit()
