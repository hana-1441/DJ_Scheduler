import os
from dotenv import load_dotenv,dotenv_values
import sys
import subprocess # to call .sh file using python
import psycopg2
import time
from datetime import datetime
# from myapp.models import Data
# from django.core.files import File
# from myproject import settings

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
import random

# global list for final pl, topic pair
global pl
pl = []

f = open("fetch_data.txt",'a+')
f.write(f"\n\n\n************{datetime.now()}**************\n")

# class for DB connect
class Util:
    def conn():
        return psycopg2.connect(host=os.getenv('HOST'),user=os.getenv('USERN'),database=os.getenv('DATABASE'),port=os.getenv('PORT'))


# calss to organize data get from .sh file
class FirstCall:
    # function to organize data fetched by .sh file 
    def home(data):
        f.write("\nHome Function called")
        print("Data : \n",data)
        print("Type : ",type(data)) # data get in type of string
        nl = data.split('\n')
        fl = nl[2:-1] # to remove unwanted lines 
        li = []
        for i in fl:
            li.append(i.strip())
        for i in li:
            x = i.split('|')
            pl.append([x[0].strip(),x[1].strip()])

        print(pl)
        f.write(f"\nextracted data list pair of pl & topic : {pl}")

# class to work on selenium using pl & topic given
class WorkSelenium:
    # funciton to apply pl & topic using selenium to get rest of info from site & store to DB
    def fetch_data(pl,tp):

        f.write("\nfetch_data Function called \n")
        options = Options()
        # options = FirefoxOptions()
        options.add_argument('--headless')
        f.write("\nheadless options run success")
        

        ran_num = random.randint(1,100)
            
    #     data = Data.objects.get(pl=pl,topic=tp)
        
    #     # update staus in DB to know work has been started on them
    #     data.status="in_process"
    #     data.save()

        driver = webdriver.Firefox(options=options)
        driver.get('https://www.w3schools.com/')
        f.write("\ndriver created and URL get")
        

        # element from all prog lang menu
        # QUERY : can't click element which are not present in current window
        tpq = driver.find_element(By.LINK_TEXT,pl.upper()).click()
        
        
        # find slider bar
        slider = driver.find_element(By.XPATH , "//div[@id='leftmenuinnerinner']")
        

        # topic find
        try:
            # this block for normal case of topic as Python Variable, Java Syntax, etc..
            tp1 = slider.find_element(By.PARTIAL_LINK_TEXT, tp.title())
            tp1.click()

        except:
            # this block works in case of topic as JS Intro, PHP syntax, SQL Basic Concepts, etc...
            x=''
            ex_li=[1]
            in_li = tp.split(' ')
            ex_li[0]=in_li[0].upper()
            for xi in in_li[1:]:
                ex_li.append(xi.capitalize())
            x=" ".join(ex_li)      

            # print("New List problem : ",ex_li)
            print("New user req : ",x)
            tp2 = slider.find_element(By.PARTIAL_LINK_TEXT, x)
            tp2.click()


        # html page content
        selective_source = driver.find_element(By.CSS_SELECTOR, "#main").get_attribute("innerHTML")
        time.sleep(2)

        # examples
        examples = driver.find_elements(By.TAG_NAME, "code")
        exs=[]
        for ex in examples:
            exs.append(ex.text)

        
        time.sleep(2)

        # html file generation
        # f1 = open(f"{settings.MEDIA_ROOT}/file{tp}.html",'w')
        # f1.write(selective_source)
        # f1.close()

        # time_out mentioned
        time_out=datetime.now().strftime("%H : %M : %S")

        f.write("\nTime Out Done")

        html_data = str(selective_source)
        ex_str = str(", ".join(str(i) for i in exs))
        str_time_out = str(time_out)

        # store to DB 
        con = Util.conn()
        cursor = con.cursor()
        query = "update myapp_data set status='Done',html_doc=%s,examples=%s,time_out=%s where pl=%s and topic=%s"
        args = (html_data[:99999],ex_str,str_time_out,pl,tp)
        cursor.execute(query,args)
        con.commit()
        con.close()

        f.write("\nDatabase Updated !!!")

    #     f1 = open(f"{settings.MEDIA_ROOT}/file{tp}.html",'rb')
    #     data.html_doc = File(f1,name="file.html")
    #     data.status = "Done"
    #     data.examples = exs
    #     data.time_out = time_out
    #     data.save()

        # this will call .sh file and pass params to .sh file  
        subprocess.call(['bash','./update.sh',pl,tp,html_data,ex_str,str_time_out]) 

        driver.quit()
        f.write("\ndriver quit\n")

if __name__=="__main__":
    load_dotenv()
    FirstCall.home(sys.argv[1])
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>host : ",os.getenv("HOST"))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>user : ",os.getenv("USERN"))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>db : ",os.getenv("DATABASE"))
    for i in pl:
        print(">>>>>>>>>>>>>>>>>>>>>prog lan : ",i[0])
        print(">>>>>>>>>>>>>>>>>>>>>tpq : ",i[1])
        WorkSelenium.fetch_data(i[0],i[1]) 
        # here,
        # i[0] = prog lang
        # i[1] = topic (after data extracted from DB & manipulated the get stored in list pl)